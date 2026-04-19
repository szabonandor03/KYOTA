from __future__ import annotations

import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
KYOTA_WIKI_DIR = REPO_ROOT / "kyota-wiki"

sys.path.insert(0, str(SRC_DIR))

import kyota.core as core  # noqa: E402
from kyota.core import (  # noqa: E402
    active_claims,
    active_claim_states,
    build_dashboard_snapshot,
    list_repo_files,
    latest_unresolved_blockers,
    load_records,
    resolve_workspace,
    unresolved_blocker_states,
    workspace_summary_lines,
)


TEST_TZ = timezone(timedelta(hours=2))


def make_workspace(tmp_path: Path) -> Path:
    workspace_root = tmp_path / "workspace"
    shutil.copytree(KYOTA_WIKI_DIR, workspace_root / "kyota-wiki")
    prepare_workspace(workspace_root)
    return workspace_root


def prepare_workspace(workspace_root: Path) -> None:
    wiki_root = workspace_root / "kyota-wiki"
    sync_registry(wiki_root / "entities")
    sync_registry(wiki_root / "raw")
    reset_log(wiki_root / "log.md")


def sync_registry(directory: Path) -> None:
    entries = sorted(path.name for path in directory.glob("*.md") if path.name != "index.md")
    lines = ["# Index", ""]
    lines.extend(f"- [{name}]({name})" for name in entries)
    lines.append("")
    (directory / "index.md").write_text("\n".join(lines), encoding="utf-8")


def reset_log(log_path: Path) -> None:
    log_path.write_text(
        "\n".join(
            [
                "# KYOTA Log",
                "",
                "## Records",
                "- `timestamp=2026-04-17T19:00:00+02:00 | type=HISTORY | agent=system | "
                "worktree_or_branch=main | files_owned=- | status=done | audience=all | "
                "note=seed workspace for tests`",
                "",
            ]
        ),
        encoding="utf-8",
    )


def append_record(workspace_root: Path, record: str) -> None:
    log_path = workspace_root / "kyota-wiki" / "log.md"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(record + "\n")


def iso_at(year: int, month: int, day: int, hour: int, minute: int = 0) -> str:
    return datetime(year, month, day, hour, minute, tzinfo=TEST_TZ).replace(microsecond=0).isoformat()


def structured_record(
    *,
    timestamp: str,
    record_type: str,
    agent: str,
    files_owned: str,
    status: str,
    audience: str,
    note: str,
    worktree_or_branch: str = "main",
) -> str:
    return (
        f"- `timestamp={timestamp} | type={record_type} | agent={agent} | "
        f"worktree_or_branch={worktree_or_branch} | files_owned={files_owned} | "
        f"status={status} | audience={audience} | note={note}`"
    )


def test_resolve_workspace_from_env(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))

    workspace = resolve_workspace()

    assert workspace.repo_root == workspace_root
    assert workspace.kyota_root == workspace_root / "kyota-wiki"


def test_load_records_parses_current_log(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))

    records = load_records(resolve_workspace())

    assert records
    assert any(record.type == "HISTORY" for record in records)


def test_active_claims_and_blockers_derive_current_state(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T20:00:00+02:00 | type=CLAIM | agent=codex | worktree_or_branch=main | "
        "files_owned=kyota-wiki/index.md | status=active | audience=all | note=test claim`",
    )
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T20:00:01+02:00 | type=BLOCKER | agent=codex | worktree_or_branch=main | "
        "files_owned=kyota-wiki/index.md | status=blocked | audience=all | note=test blocker`",
    )

    records = load_records(resolve_workspace())

    active = active_claims(records)
    blockers = latest_unresolved_blockers(records)

    assert len(active) == 1
    assert len(blockers) == 1
    assert next(iter(active.values())).note == "test claim"
    assert next(iter(blockers.values())).note == "test blocker"


def test_dashboard_snapshot_generation_on_healthy_workspace(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))

    snapshot = build_dashboard_snapshot()

    assert snapshot.workspace_root == workspace_root
    assert snapshot.is_healthy
    assert snapshot.required_files_present
    assert snapshot.log_is_readable
    assert snapshot.routers_in_parity
    assert not snapshot.active_claims
    assert not snapshot.claim_states
    assert not snapshot.blockers
    assert snapshot.recent_records
    assert snapshot.next_step == "Workspace is clear. Start with `kyota tui` or `kyota status`, then claim the files you need."


def test_workspace_summary_lines_describe_ready_workspace(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))

    lines = workspace_summary_lines(build_dashboard_snapshot())
    rendered = "\n".join(lines)

    assert "KYOTA doctor passed." in rendered
    assert "workspace is healthy and ready" in rendered
    assert "no blockers are open" in rendered
    assert "no files are currently owned" in rendered


def test_active_claim_states_capture_verify_status(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T20:00:00+02:00 | type=CLAIM | agent=codex | worktree_or_branch=main | "
        "files_owned=kyota-wiki/index.md | status=active | audience=all | note=test claim`",
    )
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T20:00:01+02:00 | type=VERIFY | agent=codex | worktree_or_branch=main | "
        "files_owned=kyota-wiki/index.md | status=passed | audience=all | note=test verify`",
    )

    records = load_records(resolve_workspace())
    claim_states = active_claim_states(records)

    assert len(claim_states) == 1
    assert claim_states[0].is_verified is True
    assert claim_states[0].verification_label == "Verified"
    assert claim_states[0].release_eligible is True


def test_active_claim_states_track_last_activity_and_staleness(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    append_record(
        workspace_root,
        structured_record(
            timestamp=iso_at(2026, 4, 17, 20, 0),
            record_type="CLAIM",
            agent="codex",
            files_owned="kyota-wiki/index.md",
            status="active",
            audience="all",
            note="test claim",
        ),
    )
    append_record(
        workspace_root,
        structured_record(
            timestamp=iso_at(2026, 4, 17, 21, 0),
            record_type="VERIFY",
            agent="codex",
            files_owned="kyota-wiki/index.md",
            status="passed",
            audience="all",
            note="verified",
        ),
    )
    append_record(
        workspace_root,
        structured_record(
            timestamp=iso_at(2026, 4, 17, 22, 0),
            record_type="BLOCKER",
            agent="codex",
            files_owned="kyota-wiki/index.md",
            status="blocked",
            audience="all",
            note="waiting",
        ),
    )
    append_record(
        workspace_root,
        structured_record(
            timestamp=iso_at(2026, 4, 17, 23, 0),
            record_type="UNBLOCK",
            agent="codex",
            files_owned="kyota-wiki/index.md",
            status="done",
            audience="all",
            note="resolved",
        ),
    )
    monkeypatch.setattr(core, "current_time", lambda: datetime(2026, 4, 19, 3, 0, tzinfo=TEST_TZ))

    records = load_records(resolve_workspace())
    claim_state = active_claim_states(records)[0]

    assert claim_state.is_verified is True
    assert claim_state.last_activity_at == iso_at(2026, 4, 17, 23, 0)
    assert claim_state.age == timedelta(hours=28)
    assert claim_state.has_unresolved_blocker is False
    assert claim_state.is_stale is True


def test_unresolved_blocker_states_track_stale_blockers(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    append_record(
        workspace_root,
        structured_record(
            timestamp=iso_at(2026, 4, 17, 20, 0),
            record_type="CLAIM",
            agent="codex",
            files_owned="kyota-wiki/index.md",
            status="active",
            audience="all",
            note="claim",
        ),
    )
    append_record(
        workspace_root,
        structured_record(
            timestamp=iso_at(2026, 4, 17, 21, 0),
            record_type="BLOCKER",
            agent="codex",
            files_owned="kyota-wiki/index.md",
            status="blocked",
            audience="all",
            note="blocked",
        ),
    )
    monkeypatch.setattr(core, "current_time", lambda: datetime(2026, 4, 19, 0, 0, tzinfo=TEST_TZ))

    records = load_records(resolve_workspace())
    blocker_state = unresolved_blocker_states(records)[0]

    assert blocker_state.last_activity_at == iso_at(2026, 4, 17, 21, 0)
    assert blocker_state.age == timedelta(hours=27)
    assert blocker_state.is_stale is True


def test_recover_records_close_active_and_blocked_state(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    append_record(
        workspace_root,
        structured_record(
            timestamp=iso_at(2026, 4, 17, 20, 0),
            record_type="CLAIM",
            agent="codex",
            files_owned="kyota-wiki/index.md",
            status="active",
            audience="all",
            note="claim",
        ),
    )
    append_record(
        workspace_root,
        structured_record(
            timestamp=iso_at(2026, 4, 17, 21, 0),
            record_type="BLOCKER",
            agent="codex",
            files_owned="kyota-wiki/index.md",
            status="blocked",
            audience="all",
            note="blocked",
        ),
    )
    append_record(
        workspace_root,
        structured_record(
            timestamp=iso_at(2026, 4, 19, 0, 0),
            record_type="RECOVER",
            agent="claude",
            files_owned="kyota-wiki/index.md",
            status="recovered",
            audience="codex",
            note="recovered abandoned scope",
        ),
    )

    snapshot = build_dashboard_snapshot()

    assert not snapshot.active_claims
    assert not snapshot.claim_states
    assert not snapshot.blockers
    assert not snapshot.blocker_states


def test_list_repo_files_prefers_wiki_files_first(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    (workspace_root / "README.md").write_text("# Workspace Readme\n", encoding="utf-8")
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))

    files = list_repo_files(resolve_workspace())

    assert "README.md" in files
    assert files[0].startswith("kyota-wiki/")
    assert files.index("README.md") > 0
