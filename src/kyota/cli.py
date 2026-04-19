#!/usr/bin/env python3
"""Installable KYOTA coordination CLI."""

from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from kyota.actions import blocker, claim, handoff, history, recover, release, unblock, verify
from kyota.core import (
    ActiveClaimState,
    BlockerState,
    KyotaError,
    active_claim_states,
    build_dashboard_snapshot,
    format_record_lines,
    normalize_files,
    require_agent,
    resolve_workspace,
    run_workspace_checks,
    unresolved_blocker_states,
    workspace_summary_lines,
    load_records,
)


def err(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def command_claim(args: argparse.Namespace) -> int:
    workspace = resolve_workspace()
    agent = require_agent(args)
    files_owned = normalize_files(args.files, workspace)
    claim(workspace, agent=agent, files_owned=files_owned, note=args.note)
    print(f"claimed {','.join(files_owned)}")
    return 0


def command_history(args: argparse.Namespace) -> int:
    workspace = resolve_workspace()
    agent = require_agent(args)
    files_owned = normalize_files(args.files, workspace)
    history(workspace, agent=agent, files_owned=files_owned, note=args.note)
    print(f"recorded history for {','.join(files_owned)}")
    return 0


def command_blocker(args: argparse.Namespace) -> int:
    workspace = resolve_workspace()
    agent = require_agent(args)
    files_owned = normalize_files(args.files, workspace)
    blocker(workspace, agent=agent, files_owned=files_owned, note=args.note, audience=args.audience)
    print(f"blocked {','.join(files_owned)}")
    return 0


def command_unblock(args: argparse.Namespace) -> int:
    workspace = resolve_workspace()
    agent = require_agent(args)
    files_owned = normalize_files(args.files, workspace)
    unblock(workspace, agent=agent, files_owned=files_owned, note=args.note)
    print(f"unblocked {','.join(files_owned)}")
    return 0


def command_handoff(args: argparse.Namespace) -> int:
    workspace = resolve_workspace()
    agent = require_agent(args)
    files_owned = normalize_files(args.files, workspace)
    handoff(workspace, agent=agent, files_owned=files_owned, target_agent=args.to, note=args.note)
    print(f"handed off {','.join(files_owned)} to {args.to}")
    return 0


def command_verify(args: argparse.Namespace) -> int:
    workspace = resolve_workspace()
    agent = require_agent(args)
    files_owned = normalize_files(args.files, workspace)
    verify(workspace, agent=agent, files_owned=files_owned, note=args.note)
    print(f"verified {','.join(files_owned)}")
    return 0


def command_release(args: argparse.Namespace) -> int:
    workspace = resolve_workspace()
    agent = require_agent(args)
    files_owned = normalize_files(args.files, workspace)
    release(
        workspace,
        agent=agent,
        files_owned=files_owned,
        note=args.note,
        allow_unverified=args.allow_unverified,
    )
    print(f"released {','.join(files_owned)}")
    return 0


def _filter_claim_states(
    claim_states: Sequence[ActiveClaimState],
    *,
    agent: Optional[str] = None,
    files_filter: Optional[set[str]] = None,
) -> list[ActiveClaimState]:
    filtered: list[ActiveClaimState] = []
    for claim_state in claim_states:
        record = claim_state.record
        if agent and record.agent != agent:
            continue
        if files_filter is not None and not files_filter.intersection(record.files_owned):
            continue
        filtered.append(claim_state)
    return filtered


def _filter_blocker_states(
    blocker_states: Sequence[BlockerState],
    *,
    agent: Optional[str] = None,
    files_filter: Optional[set[str]] = None,
) -> list[BlockerState]:
    filtered: list[BlockerState] = []
    for blocker_state in blocker_states:
        record = blocker_state.record
        if agent and record.agent != agent:
            continue
        if files_filter is not None and not files_filter.intersection(record.files_owned):
            continue
        filtered.append(blocker_state)
    return filtered


def command_status(args: argparse.Namespace) -> int:
    workspace = resolve_workspace()
    records = load_records(workspace)
    files_filter = set(normalize_files(args.files, workspace)) if args.files else None
    claim_states = _filter_claim_states(
        active_claim_states(records),
        agent=args.agent,
        files_filter=files_filter,
    )
    blocker_states = _filter_blocker_states(
        unresolved_blocker_states(records, claim_states=claim_states),
        agent=args.agent,
        files_filter=files_filter,
    )
    print("\n".join(format_record_lines(claim_states, blocker_states)))
    return 0


def command_lint(args: argparse.Namespace) -> int:
    workspace = resolve_workspace()
    errors = run_workspace_checks(workspace)
    if errors:
        print("KYOTA lint failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("KYOTA lint passed.")
    print("- required workspace files are present")
    print("- routers are in parity")
    print("- entity and raw registries cover on-disk markdown files")
    print("- log records match the canonical format")
    print("- no overlapping active claims were found")
    print("- no orphan VERIFY records were found")
    print("- blocker lifecycles are valid")
    return 0


def command_doctor(args: argparse.Namespace) -> int:
    snapshot = build_dashboard_snapshot()
    print("\n".join(workspace_summary_lines(snapshot)))
    return 1 if snapshot.health_errors else 0


def command_recover(args: argparse.Namespace) -> int:
    workspace = resolve_workspace()
    agent = require_agent(args)
    files_owned = normalize_files(args.files, workspace)
    recover(workspace, agent=agent, files_owned=files_owned, note=args.note)
    print(f"recovered {','.join(files_owned)}")
    return 0


def command_tui(args: argparse.Namespace) -> int:
    try:
        from kyota.tui import KyotaDashboardApp
    except ImportError:
        err("TUI support is not installed. Install it with `python3 -m pip install '.[tui]'`.")

    app = KyotaDashboardApp()
    app.run()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="KYOTA coordination CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    history_parser = subparsers.add_parser("history", help="append a HISTORY record")
    history_parser.add_argument("--files", nargs="+", required=True, help="repo-relative or local file paths")
    history_parser.add_argument("--note", required=True, help="history summary")
    history_parser.add_argument("--agent", help="agent id; defaults to KYOTA_AGENT")
    history_parser.set_defaults(func=command_history)

    claim_parser = subparsers.add_parser("claim", help="append a CLAIM record")
    claim_parser.add_argument("--files", nargs="+", required=True, help="repo-relative or local file paths")
    claim_parser.add_argument("--note", required=True, help="reason for the claim")
    claim_parser.add_argument("--agent", help="agent id; defaults to KYOTA_AGENT")
    claim_parser.set_defaults(func=command_claim)

    blocker_parser = subparsers.add_parser("blocker", help="append a BLOCKER record")
    blocker_parser.add_argument("--files", nargs="+", required=True, help="repo-relative or local file paths")
    blocker_parser.add_argument("--note", required=True, help="blocker summary")
    blocker_parser.add_argument("--audience", default="all", help="audience for the blocker; defaults to all")
    blocker_parser.add_argument("--agent", help="agent id; defaults to KYOTA_AGENT")
    blocker_parser.set_defaults(func=command_blocker)

    unblock_parser = subparsers.add_parser("unblock", help="append an UNBLOCK record")
    unblock_parser.add_argument("--files", nargs="+", required=True, help="repo-relative or local file paths")
    unblock_parser.add_argument("--note", required=True, help="unblock summary")
    unblock_parser.add_argument("--agent", help="agent id; defaults to KYOTA_AGENT")
    unblock_parser.set_defaults(func=command_unblock)

    handoff_parser = subparsers.add_parser("handoff", help="append HANDOFF and successor CLAIM records")
    handoff_parser.add_argument("--files", nargs="+", required=True, help="repo-relative or local file paths")
    handoff_parser.add_argument("--to", required=True, help="agent receiving ownership")
    handoff_parser.add_argument("--note", required=True, help="handoff summary")
    handoff_parser.add_argument("--agent", help="current agent id; defaults to KYOTA_AGENT")
    handoff_parser.set_defaults(func=command_handoff)

    verify_parser = subparsers.add_parser("verify", help="append a VERIFY record")
    verify_parser.add_argument("--files", nargs="+", required=True, help="repo-relative or local file paths")
    verify_parser.add_argument("--note", required=True, help="verification summary")
    verify_parser.add_argument("--agent", help="agent id; defaults to KYOTA_AGENT")
    verify_parser.set_defaults(func=command_verify)

    release_parser = subparsers.add_parser("release", help="append a RELEASE record")
    release_parser.add_argument("--files", nargs="+", required=True, help="repo-relative or local file paths")
    release_parser.add_argument("--note", required=True, help="release summary")
    release_parser.add_argument("--agent", help="agent id; defaults to KYOTA_AGENT")
    release_parser.add_argument(
        "--allow-unverified",
        action="store_true",
        help="allow release when no VERIFY exists after the active CLAIM",
    )
    release_parser.set_defaults(func=command_release)

    recover_parser = subparsers.add_parser("recover", help="append a RECOVER record for a stale active claim")
    recover_parser.add_argument("--files", nargs="+", required=True, help="repo-relative or local file paths")
    recover_parser.add_argument("--note", required=True, help="recovery summary")
    recover_parser.add_argument("--agent", help="agent id; defaults to KYOTA_AGENT")
    recover_parser.set_defaults(func=command_recover)

    status_parser = subparsers.add_parser("status", help="show active claims and unresolved blockers")
    status_parser.add_argument("--files", nargs="+", help="optional repo-relative or local file paths to filter")
    status_parser.add_argument("--agent", help="optional agent id filter")
    status_parser.set_defaults(func=command_status)

    lint_parser = subparsers.add_parser("lint", help="run workspace health checks")
    lint_parser.set_defaults(func=command_lint)

    doctor_parser = subparsers.add_parser("doctor", help="check the workspace setup and point to the next step")
    doctor_parser.set_defaults(func=command_doctor)

    tui_parser = subparsers.add_parser("tui", help="launch the KYOTA coordination dashboard")
    tui_parser.set_defaults(func=command_tui)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except KyotaError as exc:
        err(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
