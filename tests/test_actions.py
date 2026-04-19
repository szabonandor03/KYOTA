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
from kyota.actions import blocker, claim, handoff, history, recover, release, unblock  # noqa: E402
from kyota.core import (  # noqa: E402
    KyotaError,
    active_claims,
    latest_unresolved_blockers,
    load_records,
    resolve_workspace,
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


def timestamp_at(year: int, month: int, day: int, hour: int, minute: int = 0) -> datetime:
    return datetime(year, month, day, hour, minute, tzinfo=TEST_TZ)


def test_action_history_appends_record(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))

    workspace = resolve_workspace()
    result = history(
        workspace,
        agent="codex",
        files_owned=("kyota-wiki/index.md",),
        note="maintenance note",
    )

    records = load_records(workspace)

    assert result.files_owned == ("kyota-wiki/index.md",)
    assert records[-1].type == "HISTORY"
    assert records[-1].note == "maintenance note"


def test_action_claim_rejects_overlap(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))

    workspace = resolve_workspace()
    claim(workspace, agent="codex", files_owned=("kyota-wiki/index.md",), note="first claim")

    try:
        claim(workspace, agent="claude", files_owned=("kyota-wiki/index.md",), note="second claim")
    except KyotaError as exc:
        assert "overlapping active claim detected" in str(exc)
    else:
        raise AssertionError("expected overlap rejection")


def test_action_blocker_requires_matching_active_claim(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))

    workspace = resolve_workspace()

    try:
        blocker(workspace, agent="codex", files_owned=("kyota-wiki/index.md",), note="need help")
    except KyotaError as exc:
        assert "no active claim matches this exact file set" in str(exc)
    else:
        raise AssertionError("expected blocker validation error")


def test_action_unblock_requires_unresolved_blocker(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))

    workspace = resolve_workspace()
    claim(workspace, agent="codex", files_owned=("kyota-wiki/index.md",), note="claim")

    try:
        unblock(workspace, agent="codex", files_owned=("kyota-wiki/index.md",), note="not blocked")
    except KyotaError as exc:
        assert "no unresolved blocker matches this exact file set" in str(exc)
    else:
        raise AssertionError("expected unblock validation error")


def test_action_handoff_creates_successor_claim(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))

    workspace = resolve_workspace()
    claim(workspace, agent="codex", files_owned=("kyota-wiki/index.md",), note="claim")
    handoff(
        workspace,
        agent="codex",
        files_owned=("kyota-wiki/index.md",),
        target_agent="claude",
        note="pass ownership",
    )

    active = active_claims(load_records(workspace))
    successor = active[("kyota-wiki/index.md",)]

    assert successor.agent == "claude"
    assert "Accepted handoff from codex" in successor.note


def test_action_release_requires_verify_unless_override(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))

    workspace = resolve_workspace()
    claim(workspace, agent="codex", files_owned=("kyota-wiki/index.md",), note="claim")

    try:
        release(workspace, agent="codex", files_owned=("kyota-wiki/index.md",), note="release")
    except KyotaError as exc:
        assert "release requires a prior VERIFY" in str(exc)
    else:
        raise AssertionError("expected release validation error")

    release(
        workspace,
        agent="codex",
        files_owned=("kyota-wiki/index.md",),
        note="force release",
        allow_unverified=True,
    )

    assert not active_claims(load_records(workspace))


def test_action_recover_rejects_non_stale_scope(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))

    workspace = resolve_workspace()
    monkeypatch.setattr(core, "current_time", lambda: timestamp_at(2026, 4, 17, 20, 0))
    claim(workspace, agent="codex", files_owned=("kyota-wiki/index.md",), note="claim")
    monkeypatch.setattr(core, "current_time", lambda: timestamp_at(2026, 4, 17, 21, 0))

    try:
        recover(workspace, agent="claude", files_owned=("kyota-wiki/index.md",), note="cleanup")
    except KyotaError as exc:
        assert "recover requires a stale active claim" in str(exc)
    else:
        raise AssertionError("expected recover validation error")


def test_action_recover_closes_stale_claim_and_blocker(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))

    workspace = resolve_workspace()
    monkeypatch.setattr(core, "current_time", lambda: timestamp_at(2026, 4, 17, 20, 0))
    claim(workspace, agent="codex", files_owned=("kyota-wiki/index.md",), note="claim")
    monkeypatch.setattr(core, "current_time", lambda: timestamp_at(2026, 4, 17, 21, 0))
    blocker(workspace, agent="codex", files_owned=("kyota-wiki/index.md",), note="blocked")
    monkeypatch.setattr(core, "current_time", lambda: timestamp_at(2026, 4, 19, 22, 0))

    result = recover(
        workspace,
        agent="claude",
        files_owned=("kyota-wiki/index.md",),
        note="recover abandoned scope",
    )

    records = load_records(workspace)

    assert result.files_owned == ("kyota-wiki/index.md",)
    assert records[-1].type == "RECOVER"
    assert records[-1].status == "recovered"
    assert records[-1].audience == "codex"
    assert not active_claims(records)
    assert not latest_unresolved_blockers(records)
