"""Pure demurrage math — no database or HTTP imports."""

from datetime import date


def get_current_calculation_date() -> date:
    """Return today's date for live dwell calculations (patchable in tests)."""
    return date.today()


def calculate_container_dwell_days(
    vessel_discharge_date: date,
    gate_out_date: date | None,
    current_calculation_date: date,
) -> int:
    """Dwell days from discharge until gate-out or the calculation date."""
    end_date = gate_out_date if gate_out_date is not None else current_calculation_date
    return max(0, (end_date - vessel_discharge_date).days)


def calculate_overdue_days_count(
    container_dwell_days: int,
    free_days_allowed: int,
) -> int:
    return max(0, container_dwell_days - free_days_allowed)


def split_tier_overdue_days(overdue_days_count: int) -> tuple[int, int]:
    """Step-tariff split: tier 1 covers days 1–5, tier 2 covers day 6+."""
    tier_1_overdue_days = min(overdue_days_count, 5)
    tier_2_overdue_days = max(0, overdue_days_count - 5)
    return tier_1_overdue_days, tier_2_overdue_days


def calculate_gross_demurrage_fee_usd(
    tier_1_overdue_days: int,
    tier_2_overdue_days: int,
    tier_1_daily_penalty_rate_usd: float,
    tier_2_daily_penalty_rate_usd: float,
    tier_discount_percentage: float,
) -> float:
    gross_before_discount = (
        tier_1_overdue_days * tier_1_daily_penalty_rate_usd
        + tier_2_overdue_days * tier_2_daily_penalty_rate_usd
    )
    return round(gross_before_discount * (1 - tier_discount_percentage), 2)


def calculate_net_payable_demurrage_fee_usd(
    gross_demurrage_fee_usd: float,
    approved_waiver_amount_usd: float,
) -> float:
    return max(0.0, round(gross_demurrage_fee_usd - approved_waiver_amount_usd, 2))


def derive_container_status_label(
    gate_out_date: date | None,
    overdue_days_count: int,
) -> str:
    if gate_out_date is not None:
        return "GATED_OUT"
    if overdue_days_count > 0:
        return "OVERDUE"
    return "IN_TERMINAL"


def build_demurrage_calculation_breakdown(
    container_identifier: str,
    vessel_discharge_date: date,
    gate_out_date: date | None,
    free_days_allowed: int,
    tier_1_daily_penalty_rate_usd: float,
    tier_2_daily_penalty_rate_usd: float,
    tier_discount_percentage: float,
    approved_waiver_amount_usd: float,
    current_calculation_date: date | None = None,
) -> dict:
    """Compose the full demurrage breakdown dictionary for API responses."""
    calculation_date = current_calculation_date or get_current_calculation_date()
    dwell_days = calculate_container_dwell_days(
        vessel_discharge_date, gate_out_date, calculation_date
    )
    overdue_days = calculate_overdue_days_count(dwell_days, free_days_allowed)
    tier_1_days, tier_2_days = split_tier_overdue_days(overdue_days)
    gross_fee = calculate_gross_demurrage_fee_usd(
        tier_1_days,
        tier_2_days,
        tier_1_daily_penalty_rate_usd,
        tier_2_daily_penalty_rate_usd,
        tier_discount_percentage,
    )
    net_fee = calculate_net_payable_demurrage_fee_usd(gross_fee, approved_waiver_amount_usd)
    return {
        "container_identifier": container_identifier,
        "container_dwell_days": dwell_days,
        "free_days_allowed": free_days_allowed,
        "overdue_days_count": overdue_days,
        "tier_1_overdue_days": tier_1_days,
        "tier_2_overdue_days": tier_2_days,
        "tier_1_daily_penalty_rate_usd": tier_1_daily_penalty_rate_usd,
        "tier_2_daily_penalty_rate_usd": tier_2_daily_penalty_rate_usd,
        "tier_discount_percentage": tier_discount_percentage,
        "gross_demurrage_fee_usd": gross_fee,
        "approved_waiver_amount_usd": approved_waiver_amount_usd,
        "net_payable_demurrage_fee_usd": net_fee,
    }
