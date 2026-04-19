from __future__ import annotations

import asyncio
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
KYOTA_WIKI_DIR = REPO_ROOT / "kyota-wiki"

sys.path.insert(0, str(SRC_DIR))

from kyota.tui import (  # noqa: E402
    BlockerModal,
    ClaimModal,
    HandoffModal,
    KyotaDashboardApp,
    NoteModal,
)
from textual.widgets import DataTable, Input, SelectionList  # noqa: E402


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


def test_auto_refresh_updates_dashboard(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    app = KyotaDashboardApp(refresh_interval=0.1)

    async def exercise() -> None:
        async with app.run_test() as pilot:
            claims_table = app.query_one("#claims-table", DataTable)
            await pilot.pause(0.2)
            assert claims_table.row_count == 1
            assert claims_table.get_row_at(0)[0] == "No active claims"

            append_record(
                workspace_root,
                "- `timestamp=2026-04-17T21:00:00+02:00 | type=CLAIM | agent=codex | worktree_or_branch=main | "
                "files_owned=kyota-wiki/index.md | status=active | audience=all | note=refresh claim`",
            )

            await pilot.pause(0.3)
            assert claims_table.row_count == 1
            assert claims_table.get_row_at(0)[0] == "codex"
            assert claims_table.get_row_at(0)[1] == "Pending"

    asyncio.run(exercise())


def test_manual_refresh_key_updates_dashboard(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    app = KyotaDashboardApp(refresh_interval=None)

    async def exercise() -> None:
        async with app.run_test() as pilot:
            claims_table = app.query_one("#claims-table", DataTable)
            await pilot.pause(0.1)
            assert claims_table.get_row_at(0)[0] == "No active claims"

            append_record(
                workspace_root,
                "- `timestamp=2026-04-17T21:00:01+02:00 | type=CLAIM | agent=codex | worktree_or_branch=main | "
                "files_owned=kyota-wiki/index.md | status=active | audience=all | note=manual refresh claim`",
            )

            await pilot.press("r")
            await pilot.pause(0.2)
            assert claims_table.get_row_at(0)[0] == "codex"

    asyncio.run(exercise())


def test_focus_moves_between_panels(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    app = KyotaDashboardApp(refresh_interval=None)

    async def exercise() -> None:
        async with app.run_test() as pilot:
            await pilot.pause(0.1)
            assert app.focused.id == "claims-table"
            await pilot.press("tab")
            assert app.focused.id == "blockers-table"
            await pilot.press("tab")
            assert app.focused.id == "records-table"

    asyncio.run(exercise())


def test_row_selection_updates_detail_pane(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T21:00:02+02:00 | type=CLAIM | agent=codex | worktree_or_branch=main | "
        "files_owned=kyota-wiki/index.md | status=active | audience=all | note=detail claim`",
    )
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T21:00:03+02:00 | type=VERIFY | agent=codex | worktree_or_branch=main | "
        "files_owned=kyota-wiki/index.md | status=passed | audience=all | note=detail verify`",
    )
    app = KyotaDashboardApp(refresh_interval=None)

    async def exercise() -> None:
        async with app.run_test() as pilot:
            await pilot.pause(0.2)
            await pilot.press("enter")
            detail = str(app.query_one("#detail-pane").content)
            assert "detail claim" in detail
            assert "Verification: Verified" in detail
            assert "Release eligible: yes" in detail

    asyncio.run(exercise())


def test_filtering_narrows_current_table(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T21:00:03+02:00 | type=CLAIM | agent=codex | worktree_or_branch=main | "
        "files_owned=kyota-wiki/index.md | status=active | audience=all | note=first claim`",
    )
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T21:00:04+02:00 | type=CLAIM | agent=claude | worktree_or_branch=main | "
        "files_owned=kyota-wiki/log.md | status=active | audience=all | note=second claim`",
    )
    app = KyotaDashboardApp(refresh_interval=None)

    async def exercise() -> None:
        async with app.run_test() as pilot:
            await pilot.pause(0.2)
            claims_table = app.query_one("#claims-table", DataTable)
            assert claims_table.row_count == 2

            await pilot.press("/")
            filter_input = app.query_one("#filter-input", Input)
            assert app.focused is filter_input
            filter_input.value = "claude"
            app.filter_text = filter_input.value
            app._render_snapshot()
            await pilot.pause(0.1)
            assert claims_table.row_count == 1
            assert claims_table.get_row_at(0)[0] == "claude"

    asyncio.run(exercise())


def test_missing_agent_disables_write_actions_and_shows_guidance(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.delenv("KYOTA_AGENT", raising=False)
    app = KyotaDashboardApp(refresh_interval=None)

    async def exercise() -> None:
        async with app.run_test() as pilot:
            await pilot.pause(0.2)
            doctor_panel = str(app.query_one("#doctor-panel").content)
            status_strip = str(app.query_one("#status-strip").content)
            detail_pane = str(app.query_one("#detail-pane").content)

            assert "Agent: not set" in doctor_panel
            assert "Write actions: disabled" in doctor_panel
            assert "export KYOTA_AGENT" in doctor_panel
            assert "Agent: not set" in status_strip
            assert "write actions are disabled" in detail_pane.lower()

            await pilot.press("c")
            await pilot.pause(0.1)
            assert not isinstance(app.screen, ClaimModal)

    asyncio.run(exercise())


def test_claim_modal_filters_files_and_creates_claim(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    (workspace_root / "README.md").write_text("# Root Readme\n", encoding="utf-8")
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    app = KyotaDashboardApp(refresh_interval=None)

    async def exercise() -> None:
        async with app.run_test() as pilot:
            await pilot.pause(0.2)
            await pilot.press("c")
            await pilot.pause(0.1)

            assert isinstance(app.screen, ClaimModal)
            modal = app.screen
            file_list = modal.query_one("#claim-file-list", SelectionList)
            search_input = modal.query_one("#claim-search-input", Input)
            note_input = modal.query_one("#claim-note-input", Input)

            first_option = str(file_list.get_option_at_index(0).prompt)
            assert first_option.startswith("kyota-wiki/")
            assert any(str(file_list.get_option_at_index(index).prompt) == "README.md" for index in range(file_list.option_count))

            search_input.value = "md"
            modal._refresh_file_options()
            file_list.select("kyota-wiki/index.md")
            file_list.select("README.md")
            note_input.value = "claim from the TUI"
            modal._submit()
            await pilot.pause(0.2)

            claims_table = app.query_one("#claims-table", DataTable)
            records_table = app.query_one("#records-table", DataTable)
            assert claims_table.row_count == 1
            assert claims_table.get_row_at(0)[0] == "codex"
            assert records_table.get_row_at(0)[0] == "CLAIM"
            assert "README.md" in claims_table.get_row_at(0)[3]

    asyncio.run(exercise())


def test_verify_works_from_selected_claim(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T21:10:00+02:00 | type=CLAIM | agent=codex | worktree_or_branch=main | "
        "files_owned=kyota-wiki/index.md | status=active | audience=all | note=verify claim`",
    )
    app = KyotaDashboardApp(refresh_interval=None)

    async def exercise() -> None:
        async with app.run_test() as pilot:
            await pilot.pause(0.2)
            await pilot.press("v")
            await pilot.pause(0.1)
            assert isinstance(app.screen, NoteModal)
            modal = app.screen
            modal.query_one("#note-input", Input).value = "checked from TUI"
            modal._submit()
            await pilot.pause(0.2)

            claims_table = app.query_one("#claims-table", DataTable)
            detail = str(app.query_one("#detail-pane").content)
            assert claims_table.get_row_at(0)[1] == "Verified"
            assert "Verification: Verified" in detail

    asyncio.run(exercise())


def test_release_is_blocked_before_verify_and_succeeds_after_verify(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T21:20:00+02:00 | type=CLAIM | agent=codex | worktree_or_branch=main | "
        "files_owned=kyota-wiki/index.md | status=active | audience=all | note=release claim`",
    )
    app = KyotaDashboardApp(refresh_interval=None)

    async def exercise() -> None:
        async with app.run_test() as pilot:
            await pilot.pause(0.2)
            await pilot.press("x")
            await pilot.pause(0.1)
            assert not isinstance(app.screen, NoteModal)
            assert app.query_one("#claims-table", DataTable).get_row_at(0)[1] == "Pending"

            await pilot.press("v")
            await pilot.pause(0.1)
            verify_modal = app.screen
            assert isinstance(verify_modal, NoteModal)
            verify_modal.query_one("#note-input", Input).value = "verified before release"
            verify_modal._submit()
            await pilot.pause(0.2)

            await pilot.press("x")
            await pilot.pause(0.1)
            release_modal = app.screen
            assert isinstance(release_modal, NoteModal)
            release_modal.query_one("#note-input", Input).value = "released from TUI"
            release_modal._submit()
            await pilot.pause(0.2)

            claims_table = app.query_one("#claims-table", DataTable)
            records_table = app.query_one("#records-table", DataTable)
            assert claims_table.get_row_at(0)[0] == "No active claims"
            assert records_table.get_row_at(0)[0] == "RELEASE"

    asyncio.run(exercise())


def test_blocker_and_unblock_work_from_selected_rows(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T21:30:00+02:00 | type=CLAIM | agent=codex | worktree_or_branch=main | "
        "files_owned=kyota-wiki/index.md | status=active | audience=all | note=blocker claim`",
    )
    app = KyotaDashboardApp(refresh_interval=None)

    async def exercise() -> None:
        async with app.run_test() as pilot:
            await pilot.pause(0.2)
            await pilot.press("b")
            await pilot.pause(0.1)
            assert isinstance(app.screen, BlockerModal)
            blocker_modal = app.screen
            blocker_modal.query_one("#blocker-audience-input", Input).value = "all"
            blocker_modal.query_one("#blocker-note-input", Input).value = "need review"
            blocker_modal._submit()
            await pilot.pause(0.2)

            blockers_table = app.query_one("#blockers-table", DataTable)
            assert blockers_table.get_row_at(0)[0] == "codex"
            assert blockers_table.get_row_at(0)[3] == "need review"

            await pilot.press("f3")
            await pilot.pause(0.1)
            await pilot.press("u")
            await pilot.pause(0.1)
            assert isinstance(app.screen, NoteModal)
            unblock_modal = app.screen
            unblock_modal.query_one("#note-input", Input).value = "review landed"
            unblock_modal._submit()
            await pilot.pause(0.2)

            assert blockers_table.get_row_at(0)[0] == "No blockers"

    asyncio.run(exercise())


def test_handoff_creates_successor_claim(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T21:40:00+02:00 | type=CLAIM | agent=codex | worktree_or_branch=main | "
        "files_owned=kyota-wiki/index.md | status=active | audience=all | note=handoff claim`",
    )
    app = KyotaDashboardApp(refresh_interval=None)

    async def exercise() -> None:
        async with app.run_test() as pilot:
            await pilot.pause(0.2)
            await pilot.press("h")
            await pilot.pause(0.1)
            assert isinstance(app.screen, HandoffModal)
            modal = app.screen
            modal.query_one("#handoff-target-input", Input).value = "claude"
            modal.query_one("#handoff-note-input", Input).value = "please continue"
            modal._submit()
            await pilot.pause(0.2)

            claims_table = app.query_one("#claims-table", DataTable)
            records_table = app.query_one("#records-table", DataTable)
            assert claims_table.get_row_at(0)[0] == "claude"
            assert records_table.get_row_at(0)[0] == "CLAIM"
            assert "Accepted handoff from codex" in claims_table.get_row_at(0)[4]

    asyncio.run(exercise())


def test_placeholder_rows_are_not_actionable(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    app = KyotaDashboardApp(refresh_interval=None)

    async def exercise() -> None:
        async with app.run_test() as pilot:
            await pilot.pause(0.2)
            assert app.query_one("#claims-table", DataTable).get_row_at(0)[0] == "No active claims"
            await pilot.press("v")
            await pilot.pause(0.1)
            assert not isinstance(app.screen, NoteModal)

    asyncio.run(exercise())


def test_broken_workspace_shows_error_state(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    (workspace_root / "kyota-wiki" / "CLAUDE.md").unlink()
    app = KyotaDashboardApp(refresh_interval=None)

    async def exercise() -> None:
        async with app.run_test() as pilot:
            await pilot.pause(0.2)
            doctor_panel = str(app.query_one("#doctor-panel").content)
            assert "Needs attention" in doctor_panel
            assert "missing CLAUDE routing file" in doctor_panel

    asyncio.run(exercise())


def test_healthy_empty_workspace_shows_ready_state_messages(tmp_path: Path, monkeypatch) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    app = KyotaDashboardApp(refresh_interval=None)

    async def exercise() -> None:
        async with app.run_test() as pilot:
            await pilot.pause(0.2)
            doctor_panel = str(app.query_one("#doctor-panel").content)
            claims_table = app.query_one("#claims-table", DataTable)
            blockers_table = app.query_one("#blockers-table", DataTable)
            records_table = app.query_one("#records-table", DataTable)
            detail_pane = str(app.query_one("#detail-pane").content)

            assert "Ready state:" in doctor_panel
            assert "Workspace is healthy and ready for coordination work." in doctor_panel
            assert "Nothing is blocked right now." in doctor_panel
            assert "No files are currently owned." in doctor_panel
            assert claims_table.get_row_at(0)[0] == "No active claims"
            assert blockers_table.get_row_at(0)[0] == "No blockers"
            assert records_table.get_row_at(0)[0] == "No recent records"
            assert "Press c to claim files" in detail_pane

    asyncio.run(exercise())


def test_tui_snapshot_healthy_empty_workspace(tmp_path: Path, monkeypatch, snap_compare) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    assert snap_compare(KyotaDashboardApp(refresh_interval=None), terminal_size=(120, 40))


def test_tui_snapshot_missing_agent_guidance(tmp_path: Path, monkeypatch, snap_compare) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.delenv("KYOTA_AGENT", raising=False)
    assert snap_compare(KyotaDashboardApp(refresh_interval=None), terminal_size=(120, 40))


def test_tui_snapshot_claim_modal(tmp_path: Path, monkeypatch, snap_compare) -> None:
    workspace_root = make_workspace(tmp_path)
    (workspace_root / "README.md").write_text("# Root Readme\n", encoding="utf-8")
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")

    async def open_claim_modal(pilot) -> None:
        await pilot.press("c")
        await pilot.pause(0.2)

    assert snap_compare(
        KyotaDashboardApp(refresh_interval=None),
        terminal_size=(120, 40),
        run_before=open_claim_modal,
    )


def test_tui_snapshot_verified_claims(tmp_path: Path, monkeypatch, snap_compare) -> None:
    workspace_root = make_workspace(tmp_path)
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T21:50:00+02:00 | type=CLAIM | agent=codex | worktree_or_branch=main | "
        "files_owned=kyota-wiki/index.md | status=active | audience=all | note=verified snapshot claim`",
    )
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T21:50:01+02:00 | type=VERIFY | agent=codex | worktree_or_branch=main | "
        "files_owned=kyota-wiki/index.md | status=passed | audience=all | note=verified snapshot note`",
    )
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    assert snap_compare(KyotaDashboardApp(refresh_interval=None), terminal_size=(120, 40))


def test_tui_snapshot_with_active_claims(tmp_path: Path, monkeypatch, snap_compare) -> None:
    workspace_root = make_workspace(tmp_path)
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T21:00:05+02:00 | type=CLAIM | agent=codex | worktree_or_branch=main | "
        "files_owned=kyota-wiki/index.md | status=active | audience=all | note=claim snapshot`",
    )
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    assert snap_compare(KyotaDashboardApp(refresh_interval=None), terminal_size=(120, 40))


def test_tui_snapshot_with_blockers(tmp_path: Path, monkeypatch, snap_compare) -> None:
    workspace_root = make_workspace(tmp_path)
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T21:00:06+02:00 | type=CLAIM | agent=codex | worktree_or_branch=main | "
        "files_owned=kyota-wiki/index.md | status=active | audience=all | note=claim for blocker snapshot`",
    )
    append_record(
        workspace_root,
        "- `timestamp=2026-04-17T21:00:07+02:00 | type=BLOCKER | agent=codex | worktree_or_branch=main | "
        "files_owned=kyota-wiki/index.md | status=blocked | audience=all | note=blocker snapshot`",
    )
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    assert snap_compare(KyotaDashboardApp(refresh_interval=None), terminal_size=(120, 40))


def test_tui_snapshot_with_workspace_failures(tmp_path: Path, monkeypatch, snap_compare) -> None:
    workspace_root = make_workspace(tmp_path)
    (workspace_root / "kyota-wiki" / "raw" / "index.md").unlink()
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    assert snap_compare(KyotaDashboardApp(refresh_interval=None), terminal_size=(120, 40))


def test_tui_snapshot_narrow_layout(tmp_path: Path, monkeypatch, snap_compare) -> None:
    workspace_root = make_workspace(tmp_path)
    monkeypatch.setenv("KYOTA_REPO_ROOT", str(workspace_root))
    monkeypatch.setenv("KYOTA_AGENT", "codex")
    assert snap_compare(KyotaDashboardApp(refresh_interval=None), terminal_size=(88, 34))
