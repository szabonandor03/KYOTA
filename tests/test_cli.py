from __future__ import annotations

import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
KYOTA_WIKI_DIR = REPO_ROOT / "kyota-wiki"
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


def iso_offset(hours: int) -> str:
    return (datetime.now(TEST_TZ) + timedelta(hours=hours)).replace(microsecond=0).isoformat()


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


def run_cli(workspace_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC_DIR) + os.pathsep + env.get("PYTHONPATH", "")
    env["KYOTA_REPO_ROOT"] = str(workspace_root)
    return subprocess.run(
        [sys.executable, "-m", "kyota.cli", *args],
        cwd=workspace_root,
        env=env,
        capture_output=True,
        text=True,
    )


def test_entrypoint_help_runs(tmp_path: Path) -> None:
    workspace_root = make_workspace(tmp_path)
    result = run_cli(workspace_root, "--help")
    assert result.returncode == 0
    assert "KYOTA coordination CLI" in result.stdout
    assert "doctor" in result.stdout
    assert "recover" in result.stdout
    assert "tui" in result.stdout


def test_overlapping_claims_are_rejected(tmp_path: Path) -> None:
    workspace_root = make_workspace(tmp_path)
    first = run_cli(
        workspace_root,
        "claim",
        "--agent",
        "codex",
        "--files",
        "kyota-wiki/index.md",
        "--note",
        "first claim",
    )
    assert first.returncode == 0

    second = run_cli(
        workspace_root,
        "claim",
        "--agent",
        "claude",
        "--files",
        "kyota-wiki/index.md",
        "--note",
        "second claim",
    )
    assert second.returncode == 1
    assert "overlapping active claim detected" in second.stderr


def test_blocker_and_unblock_flow(tmp_path: Path) -> None:
    workspace_root = make_workspace(tmp_path)
    assert run_cli(
        workspace_root,
        "claim",
        "--agent",
        "codex",
        "--files",
        "kyota-wiki/index.md",
        "--note",
        "claim for blocker flow",
    ).returncode == 0

    blocked = run_cli(
        workspace_root,
        "blocker",
        "--agent",
        "codex",
        "--files",
        "kyota-wiki/index.md",
        "--note",
        "need input",
    )
    assert blocked.returncode == 0

    status_with_blocker = run_cli(workspace_root, "status")
    assert "Unresolved blockers:" in status_with_blocker.stdout
    assert "need input" in status_with_blocker.stdout

    unblocked = run_cli(
        workspace_root,
        "unblock",
        "--agent",
        "codex",
        "--files",
        "kyota-wiki/index.md",
        "--note",
        "input received",
    )
    assert unblocked.returncode == 0

    status_after_unblock = run_cli(workspace_root, "status")
    assert "Unresolved blockers:" not in status_after_unblock.stdout


def test_handoff_creates_successor_claim(tmp_path: Path) -> None:
    workspace_root = make_workspace(tmp_path)
    assert run_cli(
        workspace_root,
        "claim",
        "--agent",
        "codex",
        "--files",
        "kyota-wiki/index.md",
        "--note",
        "claim for handoff",
    ).returncode == 0

    handoff = run_cli(
        workspace_root,
        "handoff",
        "--agent",
        "codex",
        "--to",
        "claude",
        "--files",
        "kyota-wiki/index.md",
        "--note",
        "pass to claude",
    )
    assert handoff.returncode == 0

    claude_status = run_cli(workspace_root, "status", "--agent", "claude")
    assert "Active claims:" in claude_status.stdout
    assert "agent=claude" in claude_status.stdout
    assert "Accepted handoff from codex" in claude_status.stdout


def test_release_requires_verify(tmp_path: Path) -> None:
    workspace_root = make_workspace(tmp_path)
    assert run_cli(
        workspace_root,
        "claim",
        "--agent",
        "codex",
        "--files",
        "kyota-wiki/index.md",
        "--note",
        "claim before release",
    ).returncode == 0

    release = run_cli(
        workspace_root,
        "release",
        "--agent",
        "codex",
        "--files",
        "kyota-wiki/index.md",
        "--note",
        "attempt release",
    )
    assert release.returncode == 1
    assert "release requires a prior VERIFY" in release.stderr


def test_status_renders_verify_and_stale_markers(tmp_path: Path) -> None:
    workspace_root = make_workspace(tmp_path)
    append_record(
        workspace_root,
        structured_record(
            timestamp=iso_offset(-48),
            record_type="CLAIM",
            agent="codex",
            files_owned="kyota-wiki/index.md",
            status="active",
            audience="all",
            note="stale claim",
        ),
    )
    append_record(
        workspace_root,
        structured_record(
            timestamp=iso_offset(-2),
            record_type="CLAIM",
            agent="claude",
            files_owned="kyota-wiki/log.md",
            status="active",
            audience="all",
            note="fresh claim",
        ),
    )
    append_record(
        workspace_root,
        structured_record(
            timestamp=iso_offset(-1),
            record_type="VERIFY",
            agent="claude",
            files_owned="kyota-wiki/log.md",
            status="passed",
            audience="all",
            note="verified fresh claim",
        ),
    )

    status = run_cli(workspace_root, "status")

    assert status.returncode == 0
    assert "verify=Pending" in status.stdout
    assert "verify=Verified" in status.stdout
    assert "stale=Stale" in status.stdout
    assert "stale=Fresh" in status.stdout
    assert "last_activity=" in status.stdout


def test_recover_succeeds_for_stale_scope(tmp_path: Path) -> None:
    workspace_root = make_workspace(tmp_path)
    append_record(
        workspace_root,
        structured_record(
            timestamp=iso_offset(-48),
            record_type="CLAIM",
            agent="codex",
            files_owned="kyota-wiki/index.md",
            status="active",
            audience="all",
            note="stale claim",
        ),
    )
    append_record(
        workspace_root,
        structured_record(
            timestamp=iso_offset(-47),
            record_type="BLOCKER",
            agent="codex",
            files_owned="kyota-wiki/index.md",
            status="blocked",
            audience="all",
            note="stale blocker",
        ),
    )

    recovered = run_cli(
        workspace_root,
        "recover",
        "--agent",
        "claude",
        "--files",
        "kyota-wiki/index.md",
        "--note",
        "recover abandoned scope",
    )
    assert recovered.returncode == 0
    assert "recovered kyota-wiki/index.md" in recovered.stdout

    status = run_cli(workspace_root, "status")
    assert "kyota-wiki/index.md" not in status.stdout

    log_text = (workspace_root / "kyota-wiki" / "log.md").read_text(encoding="utf-8")
    assert "type=RECOVER" in log_text
    assert "status=recovered" in log_text


def test_recover_rejects_fresh_missing_and_closed_scopes(tmp_path: Path) -> None:
    workspace_root = make_workspace(tmp_path)

    fresh_claim = run_cli(
        workspace_root,
        "claim",
        "--agent",
        "codex",
        "--files",
        "kyota-wiki/index.md",
        "--note",
        "fresh claim",
    )
    assert fresh_claim.returncode == 0

    fresh_recover = run_cli(
        workspace_root,
        "recover",
        "--agent",
        "claude",
        "--files",
        "kyota-wiki/index.md",
        "--note",
        "too early",
    )
    assert fresh_recover.returncode == 1
    assert "recover requires a stale active claim" in fresh_recover.stderr

    missing_recover = run_cli(
        workspace_root,
        "recover",
        "--agent",
        "claude",
        "--files",
        "kyota-wiki/log.md",
        "--note",
        "missing scope",
    )
    assert missing_recover.returncode == 1
    assert "no active claim matches this exact file set" in missing_recover.stderr

    released = run_cli(
        workspace_root,
        "release",
        "--agent",
        "codex",
        "--files",
        "kyota-wiki/index.md",
        "--note",
        "close claim",
        "--allow-unverified",
    )
    assert released.returncode == 0

    closed_recover = run_cli(
        workspace_root,
        "recover",
        "--agent",
        "claude",
        "--files",
        "kyota-wiki/index.md",
        "--note",
        "already closed",
    )
    assert closed_recover.returncode == 1
    assert "no active claim matches this exact file set" in closed_recover.stderr


def test_lint_passes_on_healthy_workspace(tmp_path: Path) -> None:
    workspace_root = make_workspace(tmp_path)
    lint = run_cli(workspace_root, "lint")
    assert lint.returncode == 0
    assert "KYOTA lint passed." in lint.stdout


def test_doctor_passes_and_points_to_status(tmp_path: Path) -> None:
    workspace_root = make_workspace(tmp_path)
    doctor = run_cli(workspace_root, "doctor")
    assert doctor.returncode == 0
    assert "KYOTA doctor passed." in doctor.stdout
    assert "workspace is healthy and ready" in doctor.stdout
    assert "Start with `kyota tui` or `kyota status`" in doctor.stdout


def test_doctor_surfaces_stale_work_without_failing(tmp_path: Path) -> None:
    workspace_root = make_workspace(tmp_path)
    append_record(
        workspace_root,
        structured_record(
            timestamp=iso_offset(-48),
            record_type="CLAIM",
            agent="codex",
            files_owned="kyota-wiki/index.md",
            status="active",
            audience="all",
            note="stale claim",
        ),
    )
    append_record(
        workspace_root,
        structured_record(
            timestamp=iso_offset(-47),
            record_type="BLOCKER",
            agent="codex",
            files_owned="kyota-wiki/index.md",
            status="blocked",
            audience="all",
            note="stale blocker",
        ),
    )

    doctor = run_cli(workspace_root, "doctor")

    assert doctor.returncode == 0
    assert "stale claims: 1" in doctor.stdout
    assert "stale blockers: 1" in doctor.stdout
    assert "kyota recover --files ..." in doctor.stdout
