"""Supplied synthetic records: this module makes no model or network calls."""

DEFAULT_CONTAINER = "C1"
MCP_PORT = 8871
SOURCE = "Synthetic help desk fixtures; fees are illustrative, not a tariff."

CONTAINERS = {
    "C1": {"container_identifier": "C1", "container_status_label": "OVERDUE",
           "container_dwell_days": 6, "free_days_allowed": 5},
    "C2": {"container_identifier": "C2", "container_status_label": "GATED_OUT",
           "container_dwell_days": 3, "free_days_allowed": 5},
    "C3": {"container_identifier": "C3", "container_status_label": "IN_TERMINAL",
           "container_dwell_days": 2, "free_days_allowed": 5},
}
FEES = {
    "C1": {"container_identifier": "C1", "gross_demurrage_fee_usd": 100.0,
           "approved_waiver_amount_usd": 0.0, "net_payable_demurrage_fee_usd": 100.0},
    "C2": {"container_identifier": "C2", "gross_demurrage_fee_usd": 0.0,
           "approved_waiver_amount_usd": 0.0, "net_payable_demurrage_fee_usd": 0.0},
    "C3": {"container_identifier": "C3", "gross_demurrage_fee_usd": 0.0,
           "approved_waiver_amount_usd": 0.0, "net_payable_demurrage_fee_usd": 0.0},
}


def get_container(container_id):
    print("READ container:", container_id, flush=True)
    row = CONTAINERS.get(container_id)
    return dict(row) if row else None


def get_demurrage(container_id):
    print("READ demurrage:", container_id, flush=True)
    row = FEES.get(container_id)
    return dict(row) if row else None


if __name__ == "__main__":
    print(SOURCE)
    for identifier in ["C1", "C2", "C3", "C9"]:
        print(get_container(identifier), get_demurrage(identifier))

