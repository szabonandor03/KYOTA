"""Textual coordination console for KYOTA."""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from typing import Dict, Optional, Sequence, Tuple

from textual import events, work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, DataTable, Footer, Header, Input, SelectionList, Static

from kyota.actions import (
    blocker as blocker_action,
    claim as claim_action,
    handoff as handoff_action,
    release as release_action,
    unblock as unblock_action,
    verify as verify_action,
)
from kyota.core import (
    ActiveClaimState,
    DashboardSnapshot,
    KyotaError,
    Record,
    build_dashboard_snapshot,
    list_repo_files,
    resolve_workspace,
)


@dataclass(frozen=True)
class ClaimSubmission:
    files_owned: tuple[str, ...]
    note: str


@dataclass(frozen=True)
class NoteSubmission:
    note: str


@dataclass(frozen=True)
class BlockerSubmission:
    note: str
    audience: str


@dataclass(frozen=True)
class HandoffSubmission:
    target_agent: str
    note: str


class FocusableStatic(Static, can_focus=True):
    """Static widget that participates in focus navigation."""


class SnapshotLoaded(Message):
    """Posted when a fresh workspace snapshot is available."""

    def __init__(self, snapshot: DashboardSnapshot) -> None:
        self.snapshot = snapshot
        super().__init__()


class ClaimModal(ModalScreen[Optional[ClaimSubmission]]):
    """Multi-select repo file picker for new claims."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, files: Sequence[str]) -> None:
        super().__init__()
        self.all_files = tuple(files)

    def compose(self) -> ComposeResult:
        with Container(classes="action-modal"):
            yield Static("Claim Files", classes="modal-title")
            yield Static(
                "Pick one or more repo files, add a short note, then confirm the claim.",
                classes="modal-body",
            )
            yield Input(placeholder="Filter files", id="claim-search-input")
            yield Static("", id="claim-hint", classes="modal-hint")
            yield SelectionList[str](id="claim-file-list")
            yield Input(placeholder="Why are you claiming these files?", id="claim-note-input")
            yield Static("", id="claim-error", classes="form-error")
            with Horizontal(classes="modal-actions"):
                yield Button("Claim", variant="primary", id="claim-submit")
                yield Button("Cancel", id="claim-cancel")

    def on_mount(self) -> None:
        self.styles.align = ("center", "middle")
        self._refresh_file_options()
        self.query_one("#claim-file-list", SelectionList).focus()

    def action_cancel(self) -> None:
        self.dismiss(None)

    def _refresh_file_options(self) -> None:
        search = self.query_one("#claim-search-input", Input).value.strip().lower()
        selection_list = self.query_one("#claim-file-list", SelectionList)
        previously_selected = set(selection_list.selected)
        visible_files = tuple(path for path in self.all_files if search in path.lower())
        selection_list.clear_options()
        selection_list.add_options((path, path, path in previously_selected) for path in visible_files)

        if visible_files:
            hint = f"Showing {len(visible_files)} files. Wiki files are listed first."
        else:
            hint = "No files match the current filter."
        self.query_one("#claim-hint", Static).update(hint)

    def _submit(self) -> None:
        selection_list = self.query_one("#claim-file-list", SelectionList)
        selected = tuple(sorted(selection_list.selected))
        note = self.query_one("#claim-note-input", Input).value.strip()

        if not selected:
            self.query_one("#claim-error", Static).update("Select at least one file to claim.")
            return
        if not note:
            self.query_one("#claim-error", Static).update("Add a short note before claiming the files.")
            return

        self.dismiss(ClaimSubmission(files_owned=selected, note=note))

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "claim-search-input":
            self._refresh_file_options()
            return
        if event.input.id == "claim-note-input":
            self.query_one("#claim-error", Static).update("")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "claim-search-input":
            self.query_one("#claim-file-list", SelectionList).focus()
            return
        if event.input.id == "claim-note-input":
            self._submit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "claim-submit":
            self._submit()
            return
        if event.button.id == "claim-cancel":
            self.dismiss(None)


class NoteModal(ModalScreen[Optional[NoteSubmission]]):
    """Single-note form for verify and release flows."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, *, title: str, body: str, confirm_label: str) -> None:
        super().__init__()
        self.title = title
        self.body = body
        self.confirm_label = confirm_label

    def compose(self) -> ComposeResult:
        with Container(classes="action-modal compact-modal"):
            yield Static(self.title, classes="modal-title")
            yield Static(self.body, classes="modal-body")
            yield Input(placeholder="Add a short note", id="note-input")
            yield Static("", id="note-error", classes="form-error")
            with Horizontal(classes="modal-actions"):
                yield Button(self.confirm_label, variant="primary", id="note-submit")
                yield Button("Cancel", id="note-cancel")

    def on_mount(self) -> None:
        self.styles.align = ("center", "middle")
        self.query_one("#note-input", Input).focus()

    def action_cancel(self) -> None:
        self.dismiss(None)

    def _submit(self) -> None:
        note = self.query_one("#note-input", Input).value.strip()
        if not note:
            self.query_one("#note-error", Static).update("Add a short note before continuing.")
            return
        self.dismiss(NoteSubmission(note=note))

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "note-input":
            self.query_one("#note-error", Static).update("")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "note-input":
            self._submit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "note-submit":
            self._submit()
            return
        if event.button.id == "note-cancel":
            self.dismiss(None)


class BlockerModal(ModalScreen[Optional[BlockerSubmission]]):
    """Form for blocker notes and audience."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        with Container(classes="action-modal compact-modal"):
            yield Static("Record Blocker", classes="modal-title")
            yield Static(
                "Explain what is blocked and who needs to see the blocker. "
                "Use `all` unless the blocker is aimed at someone specific.",
                classes="modal-body",
            )
            yield Input(value="all", placeholder="Audience", id="blocker-audience-input")
            yield Input(placeholder="What is blocking this claim?", id="blocker-note-input")
            yield Static("", id="blocker-error", classes="form-error")
            with Horizontal(classes="modal-actions"):
                yield Button("Block", variant="primary", id="blocker-submit")
                yield Button("Cancel", id="blocker-cancel")

    def on_mount(self) -> None:
        self.styles.align = ("center", "middle")
        self.query_one("#blocker-note-input", Input).focus()

    def action_cancel(self) -> None:
        self.dismiss(None)

    def _submit(self) -> None:
        note = self.query_one("#blocker-note-input", Input).value.strip()
        audience = self.query_one("#blocker-audience-input", Input).value.strip() or "all"
        if not note:
            self.query_one("#blocker-error", Static).update("Add a blocker note before continuing.")
            return
        self.dismiss(BlockerSubmission(note=note, audience=audience))

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id in {"blocker-note-input", "blocker-audience-input"}:
            self.query_one("#blocker-error", Static).update("")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id in {"blocker-note-input", "blocker-audience-input"}:
            self._submit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "blocker-submit":
            self._submit()
            return
        if event.button.id == "blocker-cancel":
            self.dismiss(None)


class HandoffModal(ModalScreen[Optional[HandoffSubmission]]):
    """Form for selecting the next owner of a claim."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        with Container(classes="action-modal compact-modal"):
            yield Static("Hand Off Claim", classes="modal-title")
            yield Static(
                "Choose the next agent, then add the note that explains the handoff.",
                classes="modal-body",
            )
            yield Input(placeholder="Target agent", id="handoff-target-input")
            yield Input(placeholder="Why is this claim being handed off?", id="handoff-note-input")
            yield Static("", id="handoff-error", classes="form-error")
            with Horizontal(classes="modal-actions"):
                yield Button("Hand Off", variant="primary", id="handoff-submit")
                yield Button("Cancel", id="handoff-cancel")

    def on_mount(self) -> None:
        self.styles.align = ("center", "middle")
        self.query_one("#handoff-target-input", Input).focus()

    def action_cancel(self) -> None:
        self.dismiss(None)

    def _submit(self) -> None:
        target_agent = self.query_one("#handoff-target-input", Input).value.strip()
        note = self.query_one("#handoff-note-input", Input).value.strip()

        if not target_agent:
            self.query_one("#handoff-error", Static).update("Enter the agent who should receive this claim.")
            return
        if not note:
            self.query_one("#handoff-error", Static).update("Add a short handoff note before continuing.")
            return

        self.dismiss(HandoffSubmission(target_agent=target_agent, note=note))

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id in {"handoff-target-input", "handoff-note-input"}:
            self.query_one("#handoff-error", Static).update("")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id in {"handoff-target-input", "handoff-note-input"}:
            self._submit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "handoff-submit":
            self._submit()
            return
        if event.button.id == "handoff-cancel":
            self.dismiss(None)


class KyotaDashboardApp(App[None]):
    """Operations console for KYOTA coordination work."""

    CSS_PATH = "tui.css"
    TITLE = "KYOTA Dashboard"
    SUB_TITLE = "Writable coordination console for workspace operations"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
        ("/", "focus_filter", "Filter"),
        ("c", "claim", "Claim"),
        ("v", "verify_selected", "Verify"),
        ("x", "release_selected", "Release"),
        ("b", "block_selected", "Block"),
        ("u", "unblock_selected", "Unblock"),
        ("h", "handoff_selected", "Handoff"),
        ("?", "toggle_help", "Help"),
        ("f1", "focus_doctor", "Doctor"),
        ("f2", "focus_claims", "Claims"),
        ("f3", "focus_blockers", "Blockers"),
        ("f4", "focus_records", "Recent"),
        ("f5", "focus_detail", "Detail"),
    ]

    def __init__(self, *, refresh_interval: Optional[float] = 5.0) -> None:
        super().__init__()
        self.refresh_interval = refresh_interval
        self.snapshot = build_dashboard_snapshot()
        self.filter_text = ""
        self.active_table_id = "claims-table"
        self._record_lookup: Dict[str, Dict[str, Record]] = {
            "claims-table": {},
            "blockers-table": {},
            "records-table": {},
        }
        self._claim_state_lookup: Dict[str, ActiveClaimState] = {}

    @property
    def agent(self) -> str:
        return os.getenv("KYOTA_AGENT", "").strip()

    @property
    def writes_enabled(self) -> bool:
        return bool(self.agent)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(id="status-strip")
        yield Input(placeholder="Filter the current table (/)", id="filter-input")
        with Container(id="dashboard"):
            yield FocusableStatic(id="doctor-panel")
            with Horizontal(id="upper-row"):
                with Vertical(id="claims-panel", classes="panel"):
                    yield Static("Active Claims", classes="panel-title")
                    yield DataTable(id="claims-table")
                with Vertical(id="blockers-panel", classes="panel"):
                    yield Static("Unresolved Blockers", classes="panel-title")
                    yield DataTable(id="blockers-table")
            with Horizontal(id="lower-row"):
                with Vertical(id="records-panel", classes="panel"):
                    yield Static("Recent Records", classes="panel-title")
                    yield DataTable(id="records-table")
                with Vertical(id="detail-panel", classes="panel"):
                    yield Static("Detail", classes="panel-title")
                    yield FocusableStatic(id="detail-pane")
        yield FocusableStatic(id="help-overlay", classes="hidden")
        yield Footer()

    def on_mount(self) -> None:
        self._configure_tables()
        self._sync_layout_mode(self.size.width)
        self._render_snapshot()
        self.query_one("#claims-table", DataTable).focus()
        self.active_table_id = "claims-table"
        self._sync_detail_pane()
        if self.refresh_interval:
            self.poll_snapshot()

    def on_resize(self, event: events.Resize) -> None:
        self._sync_layout_mode(event.size.width)

    def _sync_layout_mode(self, width: int) -> None:
        if width <= 110:
            self.screen.add_class("narrow")
            return
        self.screen.remove_class("narrow")

    def _configure_tables(self) -> None:
        claims = self.query_one("#claims-table", DataTable)
        claims.cursor_type = "row"
        claims.zebra_stripes = True
        claims.add_columns("Agent", "Verify", "Branch", "Files", "Note")

        blockers = self.query_one("#blockers-table", DataTable)
        blockers.cursor_type = "row"
        blockers.zebra_stripes = True
        blockers.add_columns("Agent", "Audience", "Files", "Note")

        records = self.query_one("#records-table", DataTable)
        records.cursor_type = "row"
        records.zebra_stripes = True
        records.add_columns("Type", "Agent", "Status", "Note")

    @work(exclusive=True, group="snapshot-poll")
    async def poll_snapshot(self) -> None:
        while True:
            await self._load_snapshot()
            await asyncio.sleep(self.refresh_interval or 5.0)

    @work(exclusive=True, group="snapshot-refresh")
    async def refresh_snapshot(self) -> None:
        await self._load_snapshot()

    async def _load_snapshot(self) -> None:
        snapshot = await asyncio.to_thread(build_dashboard_snapshot)
        self.post_message(SnapshotLoaded(snapshot))

    def on_snapshot_loaded(self, message: SnapshotLoaded) -> None:
        self.snapshot = message.snapshot
        self._render_snapshot()

    def _render_snapshot(self) -> None:
        self._claim_state_lookup = {
            str(claim_state.record.line_number): claim_state for claim_state in self.snapshot.claim_states
        }
        self._render_status_strip()
        self._render_doctor_panel()
        self._populate_claims_table()
        self._populate_blockers_table()
        self._populate_records_table()
        self._sync_detail_pane()
        self._render_help_overlay()

    def _render_status_strip(self) -> None:
        refresh_text = (
            f"auto-refresh every {self.refresh_interval:g}s"
            if self.refresh_interval
            else "manual refresh only"
        )
        agent_text = f"Agent: {self.agent}" if self.agent else "Agent: not set"
        write_text = "writes enabled" if self.writes_enabled else "writes disabled"
        self.query_one("#status-strip", Static).update(
            f"Workspace: {self.snapshot.workspace_name} | {agent_text} | {write_text} | {refresh_text}"
        )

    def _render_doctor_panel(self) -> None:
        lines = [
            f"Workspace: {self.snapshot.workspace_name}",
            f"Health: {'Healthy' if self.snapshot.is_healthy else 'Needs attention'}",
            f"Agent: {self.agent or 'not set'}",
            f"Write actions: {'enabled' if self.writes_enabled else 'disabled'}",
            f"Required files present: {'yes' if self.snapshot.required_files_present else 'no'}",
            f"Log readable: {'yes' if self.snapshot.log_is_readable else 'no'}",
            f"Routers in parity: {'yes' if self.snapshot.routers_in_parity else 'no'}",
            f"Active claims: {len(self.snapshot.active_claims)}",
            f"Unresolved blockers: {len(self.snapshot.blockers)}",
            "",
        ]

        if self.snapshot.health_errors:
            lines.append("Issues:")
            lines.extend(f"- {error}" for error in self.snapshot.health_errors[:5])
            if len(self.snapshot.health_errors) > 5:
                lines.append(f"- ...and {len(self.snapshot.health_errors) - 5} more")
        elif not self.snapshot.active_claims and not self.snapshot.blockers:
            lines.extend(
                [
                    "Ready state:",
                    "- Workspace is healthy and ready for coordination work.",
                    "- Nothing is blocked right now.",
                    "- No files are currently owned.",
                ]
            )
        else:
            lines.append("Issues: none")

        if not self.writes_enabled:
            lines.extend(
                [
                    "",
                    "Write guidance:",
                    "- Run `export KYOTA_AGENT=<your-name>` in this shell to enable claim, verify,",
                    "  release, blocker, unblock, and handoff actions.",
                ]
            )

        lines.extend(["", f"Next step: {self.snapshot.next_step}"])
        self.query_one("#doctor-panel", FocusableStatic).update("\n".join(lines))

    def _record_matches_filter(self, record: Record) -> bool:
        if not self.filter_text:
            return True
        haystack = " ".join(
            [
                record.type,
                record.agent,
                record.worktree_or_branch,
                record.status,
                record.audience,
                record.note,
                " ".join(record.files_owned),
            ]
        ).lower()
        return self.filter_text.lower() in haystack

    def _display_records_for(self, table_id: str, records: tuple[Record, ...]) -> list[Record]:
        if table_id != self.active_table_id or not self.filter_text:
            return list(records)
        return [record for record in records if self._record_matches_filter(record)]

    def _display_claim_states(self) -> list[ActiveClaimState]:
        claim_states = list(self.snapshot.claim_states)
        if self.active_table_id != "claims-table" or not self.filter_text:
            return claim_states
        return [state for state in claim_states if self._record_matches_filter(state.record)]

    @staticmethod
    def _is_meaningful_recent_record(record: Record) -> bool:
        return not (record.type == "HISTORY" and record.agent == "system" and not record.files_owned)

    def _placeholder_row(self, table_id: str) -> Tuple[str, ...]:
        if table_id == self.active_table_id and self.filter_text:
            if table_id == "claims-table":
                return ("No matches", "-", "-", "-", f"No rows match '{self.filter_text}'.")
            return ("No matches", "-", "-", f"No rows match '{self.filter_text}'.")
        if table_id == "claims-table":
            return ("No active claims", "-", "-", "-", "Press c to claim files when you're ready.")
        if table_id == "blockers-table":
            return ("No blockers", "-", "-", "Nothing is stalled right now.")
        return ("No recent records", "-", "-", "New claim, verify, blocker, and release activity will show here.")

    @staticmethod
    def _display_files(record: Record) -> str:
        if len(record.files_owned) <= 2:
            return ", ".join(record.files_owned)
        return f"{record.files_owned[0]}, {record.files_owned[1]}, +{len(record.files_owned) - 2} more"

    def _populate_claims_table(self) -> None:
        table = self.query_one("#claims-table", DataTable)
        table.clear(columns=False)
        self._record_lookup["claims-table"] = {}
        claim_states = self._display_claim_states()
        if not claim_states:
            table.add_row(*self._placeholder_row("claims-table"), key="claims-empty")
            return
        for claim_state in claim_states:
            record = claim_state.record
            key = str(record.line_number)
            table.add_row(
                record.agent,
                claim_state.verification_label,
                record.worktree_or_branch,
                self._display_files(record),
                record.note,
                key=key,
            )
            self._record_lookup["claims-table"][key] = record

    def _populate_blockers_table(self) -> None:
        table = self.query_one("#blockers-table", DataTable)
        table.clear(columns=False)
        self._record_lookup["blockers-table"] = {}
        records = self._display_records_for("blockers-table", self.snapshot.blockers)
        if not records:
            table.add_row(*self._placeholder_row("blockers-table"), key="blockers-empty")
            return
        for record in records:
            key = str(record.line_number)
            table.add_row(record.agent, record.audience, self._display_files(record), record.note, key=key)
            self._record_lookup["blockers-table"][key] = record

    def _populate_records_table(self) -> None:
        table = self.query_one("#records-table", DataTable)
        table.clear(columns=False)
        self._record_lookup["records-table"] = {}
        recent_records = tuple(
            record for record in self.snapshot.recent_records if self._is_meaningful_recent_record(record)
        )
        records = self._display_records_for("records-table", recent_records)
        if not records:
            table.add_row(*self._placeholder_row("records-table"), key="records-empty")
            return
        for record in records:
            key = str(record.line_number)
            table.add_row(record.type, record.agent, record.status, record.note, key=key)
            self._record_lookup["records-table"][key] = record

    def _format_record_detail(self, record: Record) -> str:
        files = "\n".join(f"- {path}" for path in record.files_owned) or "- none"
        lines = [
            f"Type: {record.type}",
            f"Agent: {record.agent}",
            f"Branch: {record.worktree_or_branch}",
            f"Status: {record.status}",
            f"Audience: {record.audience}",
            f"Timestamp: {record.timestamp}",
            f"Log line: {record.line_number}",
        ]

        claim_state = self._claim_state_lookup.get(str(record.line_number))
        if claim_state is not None:
            lines.extend(
                [
                    f"Verification: {claim_state.verification_label}",
                    f"Release eligible: {'yes' if claim_state.release_eligible else 'verify required'}",
                ]
            )

        lines.extend(["", "Files:", files, "", "Note:", record.note])
        return "\n".join(lines)

    def _sync_detail_pane(self) -> None:
        record = self._selected_record_for(self.active_table_id)
        if record is not None:
            self.query_one("#detail-pane", FocusableStatic).update(self._format_record_detail(record))
            return

        if self.snapshot.health_errors:
            self.query_one("#detail-pane", FocusableStatic).update(
                "No row is selected.\n\nUse Tab or the function keys to move between panels.\n"
                "The doctor panel above lists the current workspace issues and the next step."
            )
            return

        if self.active_table_id == "claims-table":
            if self.writes_enabled:
                detail_text = (
                    "No claim is selected.\n\n"
                    "Press c to claim files, then edit in your normal editor.\n"
                    "When the work is done, select the claim and use v to verify,\n"
                    "x to release, b to record a blocker, or h to hand it off."
                )
            else:
                detail_text = (
                    "No claim is selected.\n\n"
                    "This workspace is ready for new work, but write actions are disabled.\n"
                    "Run `export KYOTA_AGENT=<your-name>` in this shell and relaunch `kyota tui`."
                )
        elif self.active_table_id == "blockers-table":
            detail_text = (
                "No blocker is selected.\n\n"
                "Nothing is stalled right now.\n"
                "If a blocker appears here, select it and press u to unblock it."
            )
        else:
            detail_text = (
                "No recent record is selected.\n\n"
                "Recent claim, verify, blocker, handoff, and release records will appear here.\n"
                "Use / to filter the currently focused table."
            )

        self.query_one("#detail-pane", FocusableStatic).update(detail_text)

    def _selected_record_for(self, table_id: str) -> Optional[Record]:
        table = self.query_one(f"#{table_id}", DataTable)
        if table.row_count == 0:
            return None
        row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        return self._record_lookup.get(table_id, {}).get(str(row_key.value))

    def _selected_claim_state(self) -> Optional[ActiveClaimState]:
        record = self._selected_record_for("claims-table")
        if record is None:
            return None
        return self._claim_state_lookup.get(str(record.line_number))

    def _render_help_overlay(self) -> None:
        overlay = self.query_one("#help-overlay", FocusableStatic)
        overlay.update(
            "\n".join(
                [
                    "KYOTA keyboard shortcuts",
                    "",
                    "Tab / Shift+Tab  Move between panels",
                    "Arrow keys        Move inside the focused table",
                    "Enter             Refresh detail for the selected row",
                    "/                 Focus the filter input",
                    "c                 Claim files from anywhere",
                    "v / x / b / h     Verify, release, block, or hand off the selected claim",
                    "u                 Unblock the selected blocker",
                    "r                 Manual refresh",
                    "F1-F5             Jump to doctor, claims, blockers, recent, detail",
                    "?                 Toggle this help",
                    "q                 Quit",
                ]
            )
        )

    def _focus_panel(self, selector: str, panel_id: str) -> None:
        widget = self.query_one(selector)
        widget.focus()
        if panel_id in self._record_lookup:
            self.active_table_id = panel_id
            self._sync_detail_pane()

    def _notify_error(self, title: str, error: str) -> None:
        self.notify(error, title=title, severity="error")

    def _notify_disabled_writes(self) -> None:
        self.notify(
            "Write actions are disabled. Run `export KYOTA_AGENT=<your-name>` in this shell first.",
            title="Agent not set",
            severity="warning",
        )

    def _require_agent(self) -> Optional[str]:
        agent = self.agent
        if agent:
            return agent
        self._notify_disabled_writes()
        return None

    def _refresh_after_action(self, selector: str, panel_id: str) -> None:
        self.snapshot = build_dashboard_snapshot()
        self._render_snapshot()
        self._focus_panel(selector, panel_id)

    def _run_write_action(
        self,
        *,
        title: str,
        success_message: str,
        selector: str,
        panel_id: str,
        callback,
    ) -> None:
        try:
            workspace = resolve_workspace()
            callback(workspace)
        except KyotaError as exc:
            self._notify_error(title, str(exc))
            return

        self._refresh_after_action(selector, panel_id)
        self.notify(success_message, title=title, severity="information")

    def action_refresh(self) -> None:
        self.refresh_snapshot()

    def action_focus_filter(self) -> None:
        self.query_one("#filter-input", Input).focus()

    def action_toggle_help(self) -> None:
        self.query_one("#help-overlay", FocusableStatic).toggle_class("hidden")

    def action_focus_doctor(self) -> None:
        self.query_one("#doctor-panel", FocusableStatic).focus()
        self._sync_detail_pane()

    def action_focus_claims(self) -> None:
        self._focus_panel("#claims-table", "claims-table")

    def action_focus_blockers(self) -> None:
        self._focus_panel("#blockers-table", "blockers-table")

    def action_focus_records(self) -> None:
        self._focus_panel("#records-table", "records-table")

    def action_focus_detail(self) -> None:
        self.query_one("#detail-pane", FocusableStatic).focus()

    def action_claim(self) -> None:
        agent = self._require_agent()
        if not agent:
            return

        try:
            workspace = resolve_workspace()
            repo_files = list_repo_files(workspace)
        except KyotaError as exc:
            self._notify_error("Claim", str(exc))
            return

        self.push_screen(ClaimModal(repo_files), self._handle_claim_submission)

    def _handle_claim_submission(self, submission: Optional[ClaimSubmission]) -> None:
        if submission is None:
            return

        agent = self._require_agent()
        if not agent:
            return

        self._run_write_action(
            title="Claim",
            success_message=f"Claimed {', '.join(submission.files_owned)}.",
            selector="#claims-table",
            panel_id="claims-table",
            callback=lambda workspace: claim_action(
                workspace,
                agent=agent,
                files_owned=submission.files_owned,
                note=submission.note,
            ),
        )

    def _require_selected_claim(self, action_title: str) -> Optional[ActiveClaimState]:
        if self.active_table_id != "claims-table":
            self.notify(
                "Focus the claims table and select a real claim first.",
                title=action_title,
                severity="warning",
            )
            return None
        claim_state = self._selected_claim_state()
        if claim_state is None:
            self.notify(
                "Select a real claim row before using this action.",
                title=action_title,
                severity="warning",
            )
            return None
        return claim_state

    def _require_selected_blocker(self, action_title: str) -> Optional[Record]:
        if self.active_table_id != "blockers-table":
            self.notify(
                "Focus the blockers table and select a real blocker first.",
                title=action_title,
                severity="warning",
            )
            return None
        blocker_record = self._selected_record_for("blockers-table")
        if blocker_record is None:
            self.notify(
                "Select a real blocker row before using this action.",
                title=action_title,
                severity="warning",
            )
            return None
        return blocker_record

    def action_verify_selected(self) -> None:
        agent = self._require_agent()
        claim_state = self._require_selected_claim("Verify")
        if not agent or claim_state is None:
            return

        self.push_screen(
            NoteModal(
                title="Verify Claim",
                body="Record the check that tells the rest of the workspace this claim was verified.",
                confirm_label="Verify",
            ),
            lambda submission: self._handle_verify_submission(claim_state, submission),
        )

    def _handle_verify_submission(
        self,
        claim_state: ActiveClaimState,
        submission: Optional[NoteSubmission],
    ) -> None:
        if submission is None:
            return
        agent = self._require_agent()
        if not agent:
            return

        self._run_write_action(
            title="Verify",
            success_message=f"Verified {', '.join(claim_state.record.files_owned)}.",
            selector="#claims-table",
            panel_id="claims-table",
            callback=lambda workspace: verify_action(
                workspace,
                agent=agent,
                files_owned=claim_state.record.files_owned,
                note=submission.note,
            ),
        )

    def action_release_selected(self) -> None:
        agent = self._require_agent()
        claim_state = self._require_selected_claim("Release")
        if not agent or claim_state is None:
            return
        if not claim_state.is_verified:
            self.notify(
                "This claim still needs a VERIFY. Unverified release override stays CLI-only in v2.",
                title="Release blocked",
                severity="warning",
            )
            return

        self.push_screen(
            NoteModal(
                title="Release Claim",
                body="Release this verified claim so the files are available to the workspace again.",
                confirm_label="Release",
            ),
            lambda submission: self._handle_release_submission(claim_state, submission),
        )

    def _handle_release_submission(
        self,
        claim_state: ActiveClaimState,
        submission: Optional[NoteSubmission],
    ) -> None:
        if submission is None:
            return
        agent = self._require_agent()
        if not agent:
            return

        self._run_write_action(
            title="Release",
            success_message=f"Released {', '.join(claim_state.record.files_owned)}.",
            selector="#claims-table",
            panel_id="claims-table",
            callback=lambda workspace: release_action(
                workspace,
                agent=agent,
                files_owned=claim_state.record.files_owned,
                note=submission.note,
            ),
        )

    def action_block_selected(self) -> None:
        agent = self._require_agent()
        claim_state = self._require_selected_claim("Blocker")
        if not agent or claim_state is None:
            return

        self.push_screen(BlockerModal(), lambda submission: self._handle_blocker_submission(claim_state, submission))

    def _handle_blocker_submission(
        self,
        claim_state: ActiveClaimState,
        submission: Optional[BlockerSubmission],
    ) -> None:
        if submission is None:
            return
        agent = self._require_agent()
        if not agent:
            return

        self._run_write_action(
            title="Blocker",
            success_message=f"Blocked {', '.join(claim_state.record.files_owned)}.",
            selector="#blockers-table",
            panel_id="blockers-table",
            callback=lambda workspace: blocker_action(
                workspace,
                agent=agent,
                files_owned=claim_state.record.files_owned,
                note=submission.note,
                audience=submission.audience,
            ),
        )

    def action_unblock_selected(self) -> None:
        agent = self._require_agent()
        blocker_record = self._require_selected_blocker("Unblock")
        if not agent or blocker_record is None:
            return

        self.push_screen(
            NoteModal(
                title="Unblock Claim",
                body="Record the note that explains how this blocker was cleared.",
                confirm_label="Unblock",
            ),
            lambda submission: self._handle_unblock_submission(blocker_record, submission),
        )

    def _handle_unblock_submission(
        self,
        blocker_record: Record,
        submission: Optional[NoteSubmission],
    ) -> None:
        if submission is None:
            return
        agent = self._require_agent()
        if not agent:
            return

        self._run_write_action(
            title="Unblock",
            success_message=f"Unblocked {', '.join(blocker_record.files_owned)}.",
            selector="#blockers-table",
            panel_id="blockers-table",
            callback=lambda workspace: unblock_action(
                workspace,
                agent=agent,
                files_owned=blocker_record.files_owned,
                note=submission.note,
            ),
        )

    def action_handoff_selected(self) -> None:
        agent = self._require_agent()
        claim_state = self._require_selected_claim("Handoff")
        if not agent or claim_state is None:
            return

        self.push_screen(HandoffModal(), lambda submission: self._handle_handoff_submission(claim_state, submission))

    def _handle_handoff_submission(
        self,
        claim_state: ActiveClaimState,
        submission: Optional[HandoffSubmission],
    ) -> None:
        if submission is None:
            return
        agent = self._require_agent()
        if not agent:
            return

        self._run_write_action(
            title="Handoff",
            success_message=(
                f"Handed off {', '.join(claim_state.record.files_owned)} to {submission.target_agent}."
            ),
            selector="#claims-table",
            panel_id="claims-table",
            callback=lambda workspace: handoff_action(
                workspace,
                agent=agent,
                files_owned=claim_state.record.files_owned,
                target_agent=submission.target_agent,
                note=submission.note,
            ),
        )

    def on_focus(self, event: events.Focus) -> None:
        widget = event.widget
        if isinstance(widget, DataTable) and widget.id:
            self.active_table_id = widget.id
            self._sync_detail_pane()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id != "filter-input":
            return
        self.filter_text = event.value.strip()
        self._render_snapshot()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id != "filter-input":
            return
        self._focus_panel(f"#{self.active_table_id}", self.active_table_id)

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.data_table.id and event.data_table.has_focus:
            self.active_table_id = event.data_table.id
            self._sync_detail_pane()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id and event.data_table.has_focus:
            self.active_table_id = event.data_table.id
            self._sync_detail_pane()
