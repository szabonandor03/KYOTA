"""Shared mutation actions for KYOTA coordination workflows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Tuple

from kyota.core import (
    KyotaError,
    WorkspacePaths,
    active_claims,
    active_claim_states,
    append_record,
    find_active_claim_for_scope,
    find_exact_active_claim,
    find_exact_unresolved_blocker,
    has_verify_after,
    load_records,
    overlap_for_request,
)


@dataclass(frozen=True)
class ActionResult:
    """Outcome of a successful KYOTA write action."""

    files_owned: Tuple[str, ...]
    appended_records: Tuple[str, ...]


def _append(
    workspace: WorkspacePaths,
    *,
    record_type: str,
    agent: str,
    files_owned: Sequence[str],
    status: str,
    audience: str,
    note: str,
) -> str:
    return append_record(
        workspace,
        record_type=record_type,
        agent=agent,
        files_owned=files_owned,
        status=status,
        audience=audience,
        note=note,
    )


def claim(
    workspace: WorkspacePaths,
    *,
    agent: str,
    files_owned: Tuple[str, ...],
    note: str,
) -> ActionResult:
    records = load_records(workspace)
    overlaps = overlap_for_request(files_owned, active_claims(records))
    if overlaps:
        conflict_lines = []
        for claim_record, overlap in overlaps:
            conflict_lines.append(
                f"{claim_record.agent} already owns {','.join(overlap)} "
                f"via active claim at log line {claim_record.line_number}"
            )
        raise KyotaError("overlapping active claim detected:\n- " + "\n- ".join(conflict_lines))

    return ActionResult(
        files_owned=files_owned,
        appended_records=(
            _append(
                workspace,
                record_type="CLAIM",
                agent=agent,
                files_owned=files_owned,
                status="active",
                audience="all",
                note=note,
            ),
        ),
    )


def history(
    workspace: WorkspacePaths,
    *,
    agent: str,
    files_owned: Tuple[str, ...],
    note: str,
) -> ActionResult:
    return ActionResult(
        files_owned=files_owned,
        appended_records=(
            _append(
                workspace,
                record_type="HISTORY",
                agent=agent,
                files_owned=files_owned,
                status="done",
                audience="all",
                note=note,
            ),
        ),
    )


def verify(
    workspace: WorkspacePaths,
    *,
    agent: str,
    files_owned: Tuple[str, ...],
    note: str,
) -> ActionResult:
    records = load_records(workspace)
    find_exact_active_claim(records, files_owned, agent)
    return ActionResult(
        files_owned=files_owned,
        appended_records=(
            _append(
                workspace,
                record_type="VERIFY",
                agent=agent,
                files_owned=files_owned,
                status="passed",
                audience="all",
                note=note,
            ),
        ),
    )


def release(
    workspace: WorkspacePaths,
    *,
    agent: str,
    files_owned: Tuple[str, ...],
    note: str,
    allow_unverified: bool = False,
) -> ActionResult:
    records = load_records(workspace)
    claim_record = find_exact_active_claim(records, files_owned, agent)
    if not allow_unverified and not has_verify_after(records, claim_record):
        raise KyotaError(
            "release requires a prior VERIFY for this claim; "
            "rerun with --allow-unverified to override"
        )

    return ActionResult(
        files_owned=files_owned,
        appended_records=(
            _append(
                workspace,
                record_type="RELEASE",
                agent=agent,
                files_owned=files_owned,
                status="released",
                audience="all",
                note=note,
            ),
        ),
    )


def blocker(
    workspace: WorkspacePaths,
    *,
    agent: str,
    files_owned: Tuple[str, ...],
    note: str,
    audience: str = "all",
) -> ActionResult:
    records = load_records(workspace)
    find_exact_active_claim(records, files_owned, agent)
    return ActionResult(
        files_owned=files_owned,
        appended_records=(
            _append(
                workspace,
                record_type="BLOCKER",
                agent=agent,
                files_owned=files_owned,
                status="blocked",
                audience=audience,
                note=note,
            ),
        ),
    )


def unblock(
    workspace: WorkspacePaths,
    *,
    agent: str,
    files_owned: Tuple[str, ...],
    note: str,
) -> ActionResult:
    records = load_records(workspace)
    find_exact_active_claim(records, files_owned, agent)
    find_exact_unresolved_blocker(records, files_owned, agent)
    return ActionResult(
        files_owned=files_owned,
        appended_records=(
            _append(
                workspace,
                record_type="UNBLOCK",
                agent=agent,
                files_owned=files_owned,
                status="done",
                audience="all",
                note=note,
            ),
        ),
    )


def handoff(
    workspace: WorkspacePaths,
    *,
    agent: str,
    files_owned: Tuple[str, ...],
    target_agent: str,
    note: str,
) -> ActionResult:
    records = load_records(workspace)
    find_exact_active_claim(records, files_owned, agent)
    handoff_record = _append(
        workspace,
        record_type="HANDOFF",
        agent=agent,
        files_owned=files_owned,
        status="handoff",
        audience=target_agent,
        note=note,
    )
    successor_claim = _append(
        workspace,
        record_type="CLAIM",
        agent=target_agent,
        files_owned=files_owned,
        status="active",
        audience="all",
        note=f"Accepted handoff from {agent}: {note}",
    )
    return ActionResult(
        files_owned=files_owned,
        appended_records=(handoff_record, successor_claim),
    )


def recover(
    workspace: WorkspacePaths,
    *,
    agent: str,
    files_owned: Tuple[str, ...],
    note: str,
) -> ActionResult:
    records = load_records(workspace)
    claim_record = find_active_claim_for_scope(records, files_owned)
    claim_state_by_key = {
        claim_state.record.key: claim_state
        for claim_state in active_claim_states(records)
    }
    claim_state = claim_state_by_key.get(files_owned)
    if claim_state is None or not claim_state.is_stale:
        raise KyotaError(
            "recover requires a stale active claim for this exact file set; "
            "check `kyota status` before recovering"
        )

    return ActionResult(
        files_owned=files_owned,
        appended_records=(
            _append(
                workspace,
                record_type="RECOVER",
                agent=agent,
                files_owned=files_owned,
                status="recovered",
                audience=claim_record.agent,
                note=note,
            ),
        ),
    )
