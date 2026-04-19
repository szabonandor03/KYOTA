"""Shared workspace, parsing, and snapshot logic for KYOTA."""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable, Optional, Sequence, Tuple


RECORD_RE = re.compile(
    r"^- `timestamp=(?P<timestamp>[^|]+?) \| "
    r"type=(?P<type>[^|]+?) \| "
    r"agent=(?P<agent>[^|]+?) \| "
    r"worktree_or_branch=(?P<worktree_or_branch>[^|]+?) \| "
    r"files_owned=(?P<files_owned>[^|]+?) \| "
    r"status=(?P<status>[^|]+?) \| "
    r"audience=(?P<audience>[^|]+?) \| "
    r"note=(?P<note>.*)`\s*$"
)
VALID_TYPES = {"HISTORY", "CLAIM", "BLOCKER", "UNBLOCK", "HANDOFF", "VERIFY", "RELEASE", "RECOVER"}
LIFECYCLE_END_TYPES = {"HANDOFF", "RELEASE", "RECOVER"}
STALE_AFTER = timedelta(hours=24)


class KyotaError(RuntimeError):
    """Raised when the workspace or record lifecycle is invalid."""


@dataclass(frozen=True)
class Record:
    line_number: int
    timestamp: str
    type: str
    agent: str
    worktree_or_branch: str
    files_owned: Tuple[str, ...]
    status: str
    audience: str
    note: str

    @property
    def key(self) -> Tuple[str, ...]:
        return self.files_owned


@dataclass(frozen=True)
class ActiveClaimState:
    record: Record
    is_verified: bool
    opened_at: str
    last_activity_at: str
    age: timedelta
    has_unresolved_blocker: bool
    is_stale: bool

    @property
    def verification_label(self) -> str:
        return "Verified" if self.is_verified else "Pending"

    @property
    def release_eligible(self) -> bool:
        return self.is_verified

    @property
    def staleness_label(self) -> str:
        return "Stale" if self.is_stale else "Fresh"

    @property
    def age_label(self) -> str:
        return format_age(self.age)


@dataclass(frozen=True)
class BlockerState:
    record: Record
    opened_at: str
    last_activity_at: str
    age: timedelta
    is_stale: bool

    @property
    def staleness_label(self) -> str:
        return "Stale" if self.is_stale else "Fresh"

    @property
    def age_label(self) -> str:
        return format_age(self.age)


@dataclass(frozen=True)
class WorkspacePaths:
    repo_root: Path
    kyota_root: Path
    log_path: Path
    root_index_path: Path
    entities_dir: Path
    raw_dir: Path
    schema_dir: Path
    entities_index_path: Path
    raw_index_path: Path
    maintenance_protocol_path: Path
    multi_agent_coordination_path: Path
    codex_path: Path
    claude_path: Path


@dataclass(frozen=True)
class DashboardSnapshot:
    workspace_root: Optional[Path]
    health_errors: Tuple[str, ...]
    required_files_present: bool
    log_is_readable: bool
    routers_in_parity: bool
    claim_states: Tuple[ActiveClaimState, ...]
    blocker_states: Tuple[BlockerState, ...]
    active_claims: Tuple[Record, ...]
    blockers: Tuple[Record, ...]
    recent_records: Tuple[Record, ...]
    next_step: str

    @property
    def is_healthy(self) -> bool:
        return not self.health_errors

    @property
    def workspace_name(self) -> str:
        return self.workspace_root.name if self.workspace_root else "Unavailable"

    @property
    def stale_claim_count(self) -> int:
        return sum(1 for claim_state in self.claim_states if claim_state.is_stale)

    @property
    def stale_blocker_count(self) -> int:
        return sum(1 for blocker_state in self.blocker_states if blocker_state.is_stale)


def require_agent(args: object) -> str:
    agent = getattr(args, "agent", None) or os.getenv("KYOTA_AGENT")
    if not agent:
        raise KyotaError("set --agent or KYOTA_AGENT for mutating commands")
    return agent


def build_workspace(repo_root: Path, kyota_root: Path) -> WorkspacePaths:
    schema_dir = kyota_root / "schema"
    entities_dir = kyota_root / "entities"
    raw_dir = kyota_root / "raw"
    return WorkspacePaths(
        repo_root=repo_root,
        kyota_root=kyota_root,
        log_path=kyota_root / "log.md",
        root_index_path=kyota_root / "index.md",
        entities_dir=entities_dir,
        raw_dir=raw_dir,
        schema_dir=schema_dir,
        entities_index_path=entities_dir / "index.md",
        raw_index_path=raw_dir / "index.md",
        maintenance_protocol_path=schema_dir / "maintenance_protocol.md",
        multi_agent_coordination_path=schema_dir / "multi_agent_coordination.md",
        codex_path=kyota_root / "CODEX.md",
        claude_path=kyota_root / "CLAUDE.md",
    )


def workspace_from_candidate(candidate: Path) -> Optional[WorkspacePaths]:
    candidate = candidate.resolve()
    if (candidate / "kyota-wiki").is_dir():
        return build_workspace(candidate, candidate / "kyota-wiki")
    if candidate.name == "kyota-wiki":
        return build_workspace(candidate.parent, candidate)
    return None


def resolve_workspace(explicit_root: Optional[Path] = None) -> WorkspacePaths:
    if explicit_root is not None:
        workspace = workspace_from_candidate(explicit_root)
        if workspace is None:
            raise KyotaError(
                "the supplied workspace root must be the repo root or the `kyota-wiki/` directory"
            )
        return workspace

    env_root = os.getenv("KYOTA_REPO_ROOT") or os.getenv("KYOTA_ROOT")
    if env_root:
        workspace = workspace_from_candidate(Path(env_root))
        if workspace is None:
            raise KyotaError(
                "KYOTA_REPO_ROOT/KYOTA_ROOT must point to the repo root or the `kyota-wiki/` directory"
            )
        return workspace

    for candidate in [Path.cwd().resolve(), *Path.cwd().resolve().parents]:
        workspace = workspace_from_candidate(candidate)
        if workspace is not None:
            return workspace

    dev_workspace = workspace_from_candidate(Path(__file__).resolve().parents[2])
    if dev_workspace is not None:
        return dev_workspace

    raise KyotaError(
        "could not locate a KYOTA workspace; run this command from the repo root, "
        "inside `kyota-wiki/`, or set KYOTA_REPO_ROOT"
    )


def relative_to_repo(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root).as_posix()


def run_git_stdout(workspace: WorkspacePaths, args: Sequence[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=workspace.repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return ""
    return result.stdout.strip()


def normalize_files(
    raw_files: Sequence[str], workspace: WorkspacePaths, cwd: Optional[Path] = None
) -> Tuple[str, ...]:
    base_dir = (cwd or Path.cwd()).resolve()
    try:
        base_dir.relative_to(workspace.repo_root)
    except ValueError:
        base_dir = workspace.repo_root

    seen = set()
    normalized: list[str] = []
    for raw in raw_files:
        path = Path(raw)
        if not path.is_absolute():
            path = (base_dir / path).resolve()
        else:
            path = path.resolve()
        try:
            rel = path.relative_to(workspace.repo_root).as_posix()
        except ValueError as exc:
            raise KyotaError(f"path '{raw}' is outside the repository root") from exc
        if rel not in seen:
            seen.add(rel)
            normalized.append(rel)
    if not normalized:
        raise KyotaError("at least one file must be provided")
    return tuple(sorted(normalized))


def _should_include_repo_file(path: Path, repo_root: Path) -> bool:
    rel_parts = path.relative_to(repo_root).parts
    skip_dirs = {
        ".git",
        ".hg",
        ".svn",
        ".idea",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".venv",
        "venv",
        "__pycache__",
    }
    if any(part in skip_dirs for part in rel_parts[:-1]):
        return False
    if any(part.startswith(".") for part in rel_parts):
        return False
    if path.suffix in {".pyc", ".pyo"}:
        return False
    return path.is_file()


def _repo_file_sort_key(path_str: str) -> tuple[int, str]:
    if path_str.startswith("kyota-wiki/") and path_str.endswith(".md"):
        return (0, path_str)
    if path_str.startswith("kyota-wiki/"):
        return (1, path_str)
    return (2, path_str)


def list_repo_files(workspace: WorkspacePaths) -> Tuple[str, ...]:
    tracked_files = [
        path
        for path in run_git_stdout(workspace, ["ls-files"]).splitlines()
        if path and (workspace.repo_root / path).is_file()
    ]
    if tracked_files:
        return tuple(sorted(dict.fromkeys(tracked_files), key=_repo_file_sort_key))

    files: list[str] = []
    for path in workspace.repo_root.rglob("*"):
        if not _should_include_repo_file(path, workspace.repo_root):
            continue
        files.append(path.relative_to(workspace.repo_root).as_posix())
    return tuple(sorted(files, key=_repo_file_sort_key))


def current_branch_name(workspace: WorkspacePaths) -> str:
    branch = run_git_stdout(workspace, ["symbolic-ref", "--quiet", "--short", "HEAD"])
    if not branch:
        branch = run_git_stdout(workspace, ["rev-parse", "--abbrev-ref", "HEAD"])
    if not branch or branch == "HEAD":
        return Path.cwd().name
    return branch


def current_time() -> datetime:
    return datetime.now().astimezone().replace(microsecond=0)


def now_iso8601() -> str:
    return current_time().isoformat()


def parse_timestamp(raw: str) -> datetime:
    return datetime.fromisoformat(raw)


def format_age(age: timedelta) -> str:
    total_seconds = max(int(age.total_seconds()), 0)
    days, remainder = divmod(total_seconds, 24 * 60 * 60)
    hours, remainder = divmod(remainder, 60 * 60)
    minutes = remainder // 60
    if days:
        return f"{days}d {hours}h"
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def parse_files_owned(raw: str) -> Tuple[str, ...]:
    raw = raw.strip()
    if raw == "-":
        return tuple()
    parts = [part.strip() for part in raw.split(",") if part.strip()]
    return tuple(sorted(dict.fromkeys(parts)))


def _read_text(path: Path, label: str) -> str:
    try:
        return path.read_text()
    except FileNotFoundError as exc:
        raise KyotaError(f"{label} not found at {path}") from exc
    except OSError as exc:
        raise KyotaError(f"failed to read {label} at {path}: {exc}") from exc


def load_records(workspace: WorkspacePaths) -> list[Record]:
    records: list[Record] = []
    content = _read_text(workspace.log_path, "log file")
    for idx, line in enumerate(content.splitlines(), start=1):
        match = RECORD_RE.match(line)
        if not match:
            continue
        record_type = match.group("type").strip()
        if record_type not in VALID_TYPES:
            continue
        records.append(
            Record(
                line_number=idx,
                timestamp=match.group("timestamp").strip(),
                type=record_type,
                agent=match.group("agent").strip(),
                worktree_or_branch=match.group("worktree_or_branch").strip(),
                files_owned=parse_files_owned(match.group("files_owned")),
                status=match.group("status").strip(),
                audience=match.group("audience").strip(),
                note=match.group("note").strip(),
            )
        )
    return records


def load_record_lines(workspace: WorkspacePaths) -> list[str]:
    return _read_text(workspace.log_path, "log file").splitlines()


def append_record(
    workspace: WorkspacePaths,
    *,
    record_type: str,
    agent: str,
    files_owned: Sequence[str],
    status: str,
    audience: str,
    note: str,
    worktree_or_branch: Optional[str] = None,
) -> str:
    record = (
        f"- `timestamp={now_iso8601()} | "
        f"type={record_type} | "
        f"agent={agent} | "
        f"worktree_or_branch={worktree_or_branch or current_branch_name(workspace)} | "
        f"files_owned={','.join(files_owned) if files_owned else '-'} | "
        f"status={status} | "
        f"audience={audience} | "
        f"note={note}`"
    )
    with workspace.log_path.open("a", encoding="utf-8") as handle:
        handle.write(record + "\n")
    return record


def active_claims(records: Iterable[Record]) -> dict[Tuple[str, ...], Record]:
    active: dict[Tuple[str, ...], Record] = {}
    for record in records:
        if not record.files_owned:
            continue
        if record.type == "CLAIM":
            active[record.key] = record
        elif record.type in LIFECYCLE_END_TYPES:
            active.pop(record.key, None)
    return active


def _scope_records_until_end(records: Sequence[Record], record: Record) -> Iterable[Record]:
    for candidate in records:
        if candidate.line_number <= record.line_number:
            continue
        if candidate.key != record.key:
            continue
        if candidate.type in LIFECYCLE_END_TYPES:
            return
        yield candidate


def _stale_age(last_activity_at: str, *, now: Optional[datetime] = None) -> timedelta:
    reference_now = now or current_time()
    return max(reference_now - parse_timestamp(last_activity_at), timedelta(0))


def _claim_state(record: Record, records: Sequence[Record], *, now: Optional[datetime] = None) -> ActiveClaimState:
    is_verified = False
    has_unresolved_blocker = False
    last_activity_at = record.timestamp
    for scope_record in _scope_records_until_end(records, record):
        if scope_record.agent != record.agent:
            continue
        if scope_record.type == "VERIFY":
            is_verified = True
            last_activity_at = scope_record.timestamp
        elif scope_record.type == "BLOCKER":
            has_unresolved_blocker = True
            last_activity_at = scope_record.timestamp
        elif scope_record.type == "UNBLOCK":
            has_unresolved_blocker = False
            last_activity_at = scope_record.timestamp

    age = _stale_age(last_activity_at, now=now)
    return ActiveClaimState(
        record=record,
        is_verified=is_verified,
        opened_at=record.timestamp,
        last_activity_at=last_activity_at,
        age=age,
        has_unresolved_blocker=has_unresolved_blocker,
        is_stale=age >= STALE_AFTER,
    )


def active_claim_states(records: Sequence[Record], *, now: Optional[datetime] = None) -> tuple[ActiveClaimState, ...]:
    active_records = tuple(
        sorted(active_claims(records).values(), key=lambda item: (item.timestamp, item.agent, item.files_owned))
    )
    return tuple(_claim_state(record, records, now=now) for record in active_records)


def latest_unresolved_blockers(records: Iterable[Record]) -> dict[Tuple[str, ...], Record]:
    blockers: dict[Tuple[str, ...], Record] = {}
    for record in records:
        if not record.files_owned:
            continue
        if record.type == "BLOCKER":
            blockers[record.key] = record
        elif record.type in {"UNBLOCK", *LIFECYCLE_END_TYPES}:
            blockers.pop(record.key, None)
    return blockers


def unresolved_blocker_states(
    records: Sequence[Record],
    *,
    now: Optional[datetime] = None,
    claim_states: Optional[Sequence[ActiveClaimState]] = None,
) -> tuple[BlockerState, ...]:
    claim_states = claim_states or active_claim_states(records, now=now)
    claim_state_by_key = {
        claim_state.record.key: claim_state
        for claim_state in claim_states
        if claim_state.has_unresolved_blocker
    }
    blocker_records = tuple(
        sorted(
            latest_unresolved_blockers(records).values(),
            key=lambda item: (item.timestamp, item.agent, item.files_owned),
        )
    )

    states: list[BlockerState] = []
    for blocker_record in blocker_records:
        claim_state = claim_state_by_key.get(blocker_record.key)
        last_activity_at = blocker_record.timestamp
        if claim_state is not None:
            last_activity_at = claim_state.last_activity_at
            age = claim_state.age
            is_stale = claim_state.is_stale
        else:
            age = _stale_age(last_activity_at, now=now)
            is_stale = age >= STALE_AFTER
        states.append(
            BlockerState(
                record=blocker_record,
                opened_at=blocker_record.timestamp,
                last_activity_at=last_activity_at,
                age=age,
                is_stale=is_stale,
            )
        )

    return tuple(states)


def filter_records(
    records: Iterable[Record],
    *,
    agent: Optional[str] = None,
    files_filter: Optional[set[str]] = None,
) -> list[Record]:
    filtered: list[Record] = []
    for record in records:
        if agent and record.agent != agent:
            continue
        if files_filter is not None and not files_filter.intersection(record.files_owned):
            continue
        filtered.append(record)
    return sorted(filtered, key=lambda item: (item.timestamp, item.agent, item.files_owned))


def find_active_claim_for_scope(records: Sequence[Record], files_owned: Tuple[str, ...]) -> Record:
    claim = active_claims(records).get(files_owned)
    if claim is None:
        raise KyotaError(
            "no active claim matches this exact file set; "
            "check `kyota status` before verifying, handing off, releasing, or recovering"
        )
    return claim


def find_exact_active_claim(
    records: Sequence[Record], files_owned: Tuple[str, ...], agent: str
) -> Record:
    claim = find_active_claim_for_scope(records, files_owned)
    if claim.agent != agent:
        raise KyotaError(f"active claim for this file set belongs to '{claim.agent}', not '{agent}'")
    return claim


def find_exact_unresolved_blocker(
    records: Sequence[Record], files_owned: Tuple[str, ...], agent: str
) -> Record:
    blockers = latest_unresolved_blockers(records)
    blocker = blockers.get(files_owned)
    if blocker is None:
        raise KyotaError(
            "no unresolved blocker matches this exact file set; "
            "check `kyota status` before unblocking"
        )
    if blocker.agent != agent:
        raise KyotaError(f"unresolved blocker for this file set belongs to '{blocker.agent}', not '{agent}'")
    return blocker


def has_verify_after(records: Sequence[Record], claim: Record) -> bool:
    for record in _scope_records_until_end(records, claim):
        if record.type == "VERIFY" and record.agent == claim.agent and record.key == claim.key:
            return True
    return False


def overlap_for_request(
    requested_files: Tuple[str, ...], active: dict[Tuple[str, ...], Record]
) -> list[Tuple[Record, list[str]]]:
    overlaps = []
    requested_set = set(requested_files)
    for claim in active.values():
        overlap = sorted(requested_set.intersection(claim.files_owned))
        if overlap:
            overlaps.append((claim, overlap))
    return overlaps


def path_list_without_index(directory: Path) -> list[Path]:
    return sorted(path for path in directory.glob("*.md") if path.name != "index.md")


def registry_coverage_errors(registry_path: Path, files: Sequence[Path], repo_root: Path) -> list[str]:
    content = _read_text(registry_path, "registry")
    errors: list[str] = []
    expected_names = {path.name for path in files}
    for path in files:
        if path.name not in content:
            errors.append(f"{relative_to_repo(registry_path, repo_root)} is missing {path.name}")
    linked_names = set(re.findall(r"\[([^\]]+\.md)\]\(", content))
    for name in sorted(linked_names - expected_names):
        errors.append(f"{relative_to_repo(registry_path, repo_root)} references missing file {name}")
    return errors


def router_parity_errors(workspace: WorkspacePaths) -> list[str]:
    codex_lines = _read_text(workspace.codex_path, "CODEX routing file").splitlines()
    claude_lines = _read_text(workspace.claude_path, "CLAUDE routing file").splitlines()
    if codex_lines[1:] != claude_lines[1:]:
        return ["CODEX.md and CLAUDE.md differ beyond the title line"]
    return []


def record_format_errors(workspace: WorkspacePaths) -> list[str]:
    lines = load_record_lines(workspace)
    errors: list[str] = []
    in_records = False
    for idx, line in enumerate(lines, start=1):
        if line.strip() == "## Records":
            in_records = True
            continue
        if not in_records:
            continue
        if not line.strip():
            continue
        if line.startswith("- `"):
            match = RECORD_RE.match(line)
            if not match:
                errors.append(f"log.md line {idx} does not match the canonical record format")
            elif match.group("type").strip() not in VALID_TYPES:
                errors.append(f"log.md line {idx} uses unknown record type '{match.group('type').strip()}'")
        elif line.startswith("#"):
            break
        else:
            errors.append(f"log.md line {idx} is not a structured record entry")
    return errors


def overlap_errors(records: Sequence[Record]) -> list[str]:
    errors: list[str] = []
    active = list(active_claims(records).values())
    for idx, left in enumerate(active):
        left_set = set(left.files_owned)
        for right in active[idx + 1 :]:
            overlap = sorted(left_set.intersection(right.files_owned))
            if overlap:
                errors.append(
                    "overlapping active claims: "
                    f"{left.agent} line {left.line_number} and {right.agent} line {right.line_number} "
                    f"share {','.join(overlap)}"
                )
    return errors


def orphan_verify_errors(records: Sequence[Record]) -> list[str]:
    errors: list[str] = []
    open_claims: dict[Tuple[str, ...], Record] = {}
    for record in records:
        if record.type == "CLAIM":
            open_claims[record.key] = record
        elif record.type == "VERIFY":
            claim = open_claims.get(record.key)
            if claim is None or claim.agent != record.agent:
                errors.append(
                    f"VERIFY at log line {record.line_number} has no active matching claim for "
                    f"{','.join(record.files_owned)}"
                )
        elif record.type == "RECOVER":
            open_claims.pop(record.key, None)
        elif record.type in {"HANDOFF", "RELEASE"}:
            claim = open_claims.get(record.key)
            if claim is not None and claim.agent == record.agent:
                open_claims.pop(record.key, None)
    return errors


def blocker_lifecycle_errors(records: Sequence[Record]) -> list[str]:
    errors: list[str] = []
    active_by_key: dict[Tuple[str, ...], Record] = {}
    unresolved_by_key: dict[Tuple[str, ...], Record] = {}

    for record in records:
        if not record.files_owned:
            continue

        if record.type == "CLAIM":
            active_by_key[record.key] = record
        elif record.type == "BLOCKER":
            claim = active_by_key.get(record.key)
            if claim is None or claim.agent != record.agent:
                errors.append(
                    f"BLOCKER at log line {record.line_number} has no active matching claim for "
                    f"{','.join(record.files_owned)}"
                )
            else:
                unresolved_by_key[record.key] = record
        elif record.type == "UNBLOCK":
            claim = active_by_key.get(record.key)
            blocker = unresolved_by_key.get(record.key)
            if claim is None or claim.agent != record.agent:
                errors.append(
                    f"UNBLOCK at log line {record.line_number} has no active matching claim for "
                    f"{','.join(record.files_owned)}"
                )
            elif blocker is None or blocker.agent != record.agent:
                errors.append(
                    f"UNBLOCK at log line {record.line_number} has no prior unresolved blocker for "
                    f"{','.join(record.files_owned)}"
                )
            else:
                unresolved_by_key.pop(record.key, None)
        elif record.type in LIFECYCLE_END_TYPES:
            unresolved_by_key.pop(record.key, None)
            active_by_key.pop(record.key, None)

    return errors


def required_workspace_errors(workspace: WorkspacePaths) -> list[str]:
    required_paths = [
        (workspace.root_index_path, "workspace startup manifest"),
        (workspace.log_path, "workspace log"),
        (workspace.entities_index_path, "entities index"),
        (workspace.raw_index_path, "raw index"),
        (workspace.maintenance_protocol_path, "maintenance protocol"),
        (workspace.multi_agent_coordination_path, "multi-agent coordination schema"),
        (workspace.codex_path, "CODEX routing file"),
        (workspace.claude_path, "CLAUDE routing file"),
    ]
    errors = []
    for path, label in required_paths:
        if not path.exists():
            errors.append(f"missing {label}: {relative_to_repo(path, workspace.repo_root)}")
    return errors


def run_workspace_checks(workspace: WorkspacePaths) -> list[str]:
    errors = required_workspace_errors(workspace)
    if errors:
        return errors

    records = load_records(workspace)
    entity_files = path_list_without_index(workspace.entities_dir)
    raw_files = path_list_without_index(workspace.raw_dir)

    errors.extend(record_format_errors(workspace))
    errors.extend(router_parity_errors(workspace))
    errors.extend(registry_coverage_errors(workspace.entities_index_path, entity_files, workspace.repo_root))
    errors.extend(registry_coverage_errors(workspace.raw_index_path, raw_files, workspace.repo_root))
    errors.extend(overlap_errors(records))
    errors.extend(orphan_verify_errors(records))
    errors.extend(blocker_lifecycle_errors(records))
    return errors


def recent_records(records: Sequence[Record], *, limit: int = 12) -> tuple[Record, ...]:
    return tuple(sorted(records, key=lambda record: record.line_number, reverse=True)[:limit])


def next_step_for_snapshot(
    *,
    errors: Sequence[str],
    blocker_states: Sequence[BlockerState],
    claim_states: Sequence[ActiveClaimState],
) -> str:
    if errors:
        return "Fix the workspace issues above, then rerun `kyota doctor`."
    if any(claim_state.is_stale for claim_state in claim_states) or any(
        blocker_state.is_stale for blocker_state in blocker_states
    ):
        return "Review stale work in `kyota status` or `kyota tui`, then run `kyota recover --files ...`."
    if blocker_states:
        return "Open `kyota tui` or review unresolved blockers first so you know what is stalled."
    if claim_states:
        return "Open `kyota tui` or review active claims before starting new work."
    return "Workspace is clear. Start with `kyota tui` or `kyota status`, then claim the files you need."


def build_dashboard_snapshot() -> DashboardSnapshot:
    try:
        workspace = resolve_workspace()
    except KyotaError as exc:
        return DashboardSnapshot(
            workspace_root=None,
            health_errors=(str(exc),),
            required_files_present=False,
            log_is_readable=False,
            routers_in_parity=False,
            claim_states=tuple(),
            blocker_states=tuple(),
            active_claims=tuple(),
            blockers=tuple(),
            recent_records=tuple(),
            next_step="Set KYOTA_REPO_ROOT or run the command from a KYOTA workspace.",
        )

    required_errors = required_workspace_errors(workspace)
    required_files_present = not required_errors
    log_is_readable = False
    records: list[Record] = []

    if workspace.log_path.exists():
        try:
            records = load_records(workspace)
            log_is_readable = True
        except KyotaError:
            log_is_readable = False

    routers_in_parity = False
    if workspace.codex_path.exists() and workspace.claude_path.exists():
        routers_in_parity = not router_parity_errors(workspace)

    health_errors = run_workspace_checks(workspace)
    claim_states = active_claim_states(records) if records else tuple()
    blocker_states = unresolved_blocker_states(records, claim_states=claim_states) if records else tuple()
    active = tuple(claim_state.record for claim_state in claim_states)
    blockers = tuple(blocker_state.record for blocker_state in blocker_states)

    return DashboardSnapshot(
        workspace_root=workspace.repo_root,
        health_errors=tuple(health_errors),
        required_files_present=required_files_present,
        log_is_readable=log_is_readable,
        routers_in_parity=routers_in_parity,
        claim_states=claim_states,
        blocker_states=blocker_states,
        active_claims=tuple(sorted(active, key=lambda item: (item.timestamp, item.agent, item.files_owned))),
        blockers=tuple(sorted(blockers, key=lambda item: (item.timestamp, item.agent, item.files_owned))),
        recent_records=recent_records(records),
        next_step=next_step_for_snapshot(
            errors=health_errors,
            blocker_states=blocker_states,
            claim_states=claim_states,
        ),
    )


def format_record_lines(
    claim_states: Sequence[ActiveClaimState], blocker_states: Sequence[BlockerState]
) -> list[str]:
    lines: list[str] = []
    if not claim_states:
        lines.append("No active claims.")
    else:
        lines.append("Active claims:")
        for claim_state in claim_states:
            record = claim_state.record
            lines.append(
                f"- agent={record.agent} branch={record.worktree_or_branch} "
                f"files={','.join(record.files_owned)}"
            )
            lines.append(
                "  "
                f"status={record.status} verify={claim_state.verification_label} "
                f"blocker={'open' if claim_state.has_unresolved_blocker else 'clear'} "
                f"stale={claim_state.staleness_label} age={claim_state.age_label} "
                f"line={record.line_number}"
            )
            lines.append(f"  last_activity={claim_state.last_activity_at}")
            lines.append(f"  note={record.note}")

    if blocker_states:
        lines.append("")
        lines.append("Unresolved blockers:")
        for blocker_state in blocker_states:
            record = blocker_state.record
            lines.append(
                f"- agent={record.agent} branch={record.worktree_or_branch} "
                f"files={','.join(record.files_owned)}"
            )
            lines.append(
                "  "
                f"status={record.status} stale={blocker_state.staleness_label} "
                f"age={blocker_state.age_label} line={record.line_number}"
            )
            lines.append(f"  last_activity={blocker_state.last_activity_at}")
            lines.append(f"  audience={record.audience}")
            lines.append(f"  note={record.note}")

    return lines


def workspace_summary_lines(snapshot: DashboardSnapshot) -> list[str]:
    if snapshot.health_errors:
        lines = ["KYOTA doctor found issues:"]
        lines.extend(f"- {error}" for error in snapshot.health_errors)
        lines.append("")
        lines.append(f"Next step: {snapshot.next_step}")
        return lines

    summary_lines = [
        "KYOTA doctor passed.",
        f"- workspace root: {snapshot.workspace_root}",
        "- required files are present, the log is readable, and the routers are in parity",
    ]

    if not snapshot.active_claims and not snapshot.blockers:
        summary_lines.extend(
            [
                "- workspace is healthy and ready",
                "- no blockers are open",
                "- no files are currently owned",
            ]
        )
    else:
        summary_lines.extend(
            [
                "- workspace is healthy",
                f"- active claims: {len(snapshot.active_claims)}",
                f"- unresolved blockers: {len(snapshot.blockers)}",
            ]
        )
        if snapshot.stale_claim_count or snapshot.stale_blocker_count:
            summary_lines.extend(
                [
                    f"- stale claims: {snapshot.stale_claim_count}",
                    f"- stale blockers: {snapshot.stale_blocker_count}",
                ]
            )

    summary_lines.extend(["", f"Next step: {snapshot.next_step}"])
    return summary_lines
