"""Pure dispute-claim auto-waiver decision engine — no database imports."""

from datetime import date, datetime, time, timezone

AUTO_APPROVAL_THRESHOLD_USD = 500.0

CLAIM_STATUS_SUBMITTED = "SUBMITTED"
CLAIM_STATUS_AUTO_APPROVED = "AUTO_APPROVED"
CLAIM_STATUS_ESCALATED_TO_MANAGER = "ESCALATED_TO_MANAGER"
CLAIM_STATUS_REJECTED = "REJECTED"


def evaluate_dispute_claim_decision(
    disputed_amount_usd: float,
    verified_port_exception_exists: bool,
) -> tuple[str, float]:
    """Auto-waiver state machine returning status and approved waiver amount."""
    if not verified_port_exception_exists:
        return CLAIM_STATUS_REJECTED, 0.0
    if disputed_amount_usd < AUTO_APPROVAL_THRESHOLD_USD:
        return CLAIM_STATUS_AUTO_APPROVED, round(disputed_amount_usd, 2)
    return CLAIM_STATUS_ESCALATED_TO_MANAGER, 0.0


def verify_port_exception_overlap(
    berth_terminal_name: str,
    dwell_period_start: date,
    dwell_period_end: date,
    port_exception_logs: list[dict],
) -> bool:
    """Return True when an immutable exception log overlaps the container dwell window."""
    dwell_start_timestamp = datetime.combine(
        dwell_period_start, time.min, tzinfo=timezone.utc
    )
    dwell_end_timestamp = datetime.combine(
        dwell_period_end, time.max, tzinfo=timezone.utc
    )
    for exception_log in port_exception_logs:
        if exception_log["berth_terminal_name"] != berth_terminal_name:
            continue
        exception_start = exception_log["exception_start_timestamp"]
        exception_end = exception_log["exception_end_timestamp"]
        if isinstance(exception_start, str):
            exception_start = datetime.fromisoformat(exception_start)
        if isinstance(exception_end, str):
            exception_end = datetime.fromisoformat(exception_end)
        if exception_start.tzinfo is None:
            exception_start = exception_start.replace(tzinfo=timezone.utc)
        if exception_end.tzinfo is None:
            exception_end = exception_end.replace(tzinfo=timezone.utc)
        if exception_start <= dwell_end_timestamp and exception_end >= dwell_start_timestamp:
            return True
    return False


def validate_manual_waiver_override(
    approved_waiver_amount_usd: float,
    disputed_amount_usd: float,
    claim_decision_status: str,
) -> str | None:
    """Return an error message when manager override rules are violated."""
    if claim_decision_status != CLAIM_STATUS_ESCALATED_TO_MANAGER:
        return "Manual override is only allowed for escalated claims"
    if approved_waiver_amount_usd > disputed_amount_usd:
        return "Approved waiver cannot exceed disputed amount"
    return None
