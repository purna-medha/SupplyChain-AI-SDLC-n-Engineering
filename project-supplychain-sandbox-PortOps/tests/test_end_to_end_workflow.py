"""Integration and user-journey tests for PortOps SupplyChainOps."""

from datetime import date

import pytest

from supplychainops.domain_demurrage_calculation_engine import (
    build_demurrage_calculation_breakdown,
    calculate_container_dwell_days,
    calculate_overdue_days_count,
    split_tier_overdue_days,
)
from supplychainops.domain_dispute_claims_engine import (
    evaluate_dispute_claim_decision,
    verify_port_exception_overlap,
)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "application_name": "SupplyChainOps"}


def test_list_importers(client):
    response = client.get("/importers")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_list_containers_for_importer(client):
    response = client.get("/containers", params={"importer_identifier": "IMP-GULF-001"})
    assert response.status_code == 200
    containers = response.json()
    assert len(containers) == 2
    assert {row["container_status_label"] for row in containers} == {"OVERDUE", "GATED_OUT"}


def test_list_containers_unknown_importer_returns_404(client):
    response = client.get("/containers", params={"importer_identifier": "IMP-UNKNOWN"})
    assert response.status_code == 404


def test_list_containers_status_filter(client):
    response = client.get(
        "/containers",
        params={"importer_identifier": "IMP-GULF-001", "status_filter": "OVERDUE"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["container_identifier"] == "MSKU1234567"


def test_demurrage_calculation_step_tariff_math():
    breakdown = build_demurrage_calculation_breakdown(
        container_identifier="MSKU1234567",
        vessel_discharge_date=date(2026, 9, 9),
        gate_out_date=None,
        free_days_allowed=5,
        tier_1_daily_penalty_rate_usd=150.0,
        tier_2_daily_penalty_rate_usd=250.0,
        tier_discount_percentage=0.0,
        approved_waiver_amount_usd=0.0,
        current_calculation_date=date(2026, 9, 22),
    )
    assert breakdown["container_dwell_days"] == 13
    assert breakdown["overdue_days_count"] == 8
    assert breakdown["tier_1_overdue_days"] == 5
    assert breakdown["tier_2_overdue_days"] == 3
    assert breakdown["gross_demurrage_fee_usd"] == 1500.0


def test_demurrage_calculation_api(client):
    response = client.get("/containers/MSKU1234567/demurrage-calculation")
    assert response.status_code == 200
    body = response.json()
    assert body["gross_demurrage_fee_usd"] == 1500.0
    assert body["net_payable_demurrage_fee_usd"] == 1500.0


def test_demurrage_calculation_with_platinum_discount(client):
    response = client.get("/containers/HLCU5566778/demurrage-calculation")
    assert response.status_code == 200
    body = response.json()
    assert body["tier_discount_percentage"] == 0.20
    assert body["overdue_days_count"] == 4
    assert body["gross_demurrage_fee_usd"] == 560.0


def test_gate_out_execution_success(client):
    response = client.post("/containers/TCLU9876543/gate-out-execution")
    assert response.status_code == 200
    assert response.json()["gate_out_date"] == "2026-09-22"


def test_gate_out_execution_conflict_when_already_gated_out(client):
    response = client.post("/containers/MSCU7654321/gate-out-execution")
    assert response.status_code == 409


def test_dispute_claim_auto_approved_when_exception_verified(client):
    response = client.post(
        "/dispute-claims/submit",
        json={
            "container_identifier": "MSKU1234567",
            "importer_identifier": "IMP-GULF-001",
            "disputed_amount_usd": 350.0,
            "dispute_reason_category": "CRANE_BREAKDOWN",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["claim_decision_status"] == "AUTO_APPROVED"
    assert body["approved_waiver_amount_usd"] == 350.0


def test_dispute_claim_escalated_for_large_amount(client):
    response = client.post(
        "/dispute-claims/submit",
        json={
            "container_identifier": "MSKU1234567",
            "importer_identifier": "IMP-GULF-001",
            "disputed_amount_usd": 750.0,
            "dispute_reason_category": "CRANE_BREAKDOWN",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["claim_decision_status"] == "ESCALATED_TO_MANAGER"
    assert body["approved_waiver_amount_usd"] == 0.0


def test_dispute_claim_rejected_without_exception_log(client):
    response = client.post(
        "/dispute-claims/submit",
        json={
            "container_identifier": "HLCU5566778",
            "importer_identifier": "IMP-GULF-003",
            "disputed_amount_usd": 200.0,
            "dispute_reason_category": "WEATHER_HOLD",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["claim_decision_status"] == "REJECTED"
    assert body["approved_waiver_amount_usd"] == 0.0


def test_list_dispute_claims_with_status_filter(client):
    client.post(
        "/dispute-claims/submit",
        json={
            "container_identifier": "MSKU1234567",
            "importer_identifier": "IMP-GULF-001",
            "disputed_amount_usd": 300.0,
            "dispute_reason_category": "CRANE_BREAKDOWN",
        },
    )
    response = client.get(
        "/dispute-claims",
        params={"claim_decision_status_filter": "AUTO_APPROVED"},
    )
    assert response.status_code == 200
    assert all(row["claim_decision_status"] == "AUTO_APPROVED" for row in response.json())


def test_manager_approve_override_for_escalated_claim(client):
    submit_response = client.post(
        "/dispute-claims/submit",
        json={
            "container_identifier": "MSKU1234567",
            "importer_identifier": "IMP-GULF-001",
            "disputed_amount_usd": 900.0,
            "dispute_reason_category": "CRANE_BREAKDOWN",
        },
    )
    claim_id = submit_response.json()["dispute_claim_identifier"]
    response = client.put(
        f"/dispute-claims/{claim_id}/approve-override",
        json={
            "approved_waiver_amount_usd": 600.0,
            "manager_override_note": "Partial waiver approved by terminal manager",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["approved_waiver_amount_usd"] == 600.0
    assert body["claim_decision_status"] == "AUTO_APPROVED"


def test_manager_override_rejected_for_non_escalated_claim(client):
    response = client.put(
        "/dispute-claims/1/approve-override",
        json={
            "approved_waiver_amount_usd": 100.0,
            "manager_override_note": "Should fail",
        },
    )
    assert response.status_code == 400


def test_list_drayage_jobs_and_driver_filter(client):
    response = client.get("/drayage-dispatch-jobs")
    assert response.status_code == 200
    assert len(response.json()) == 3

    filtered = client.get(
        "/drayage-dispatch-jobs",
        params={"assigned_driver_name_filter": "Ahmed Al Maktoum"},
    )
    assert filtered.status_code == 200
    assert len(filtered.json()) == 1


def test_operational_summary_metrics(client):
    response = client.get("/analytics/operational-summary")
    assert response.status_code == 200
    body = response.json()
    assert body["gross_accrued_demurrage_fees_usd"] > 0
    assert body["at_risk_container_count"] >= 2
    assert "net_demurrage_revenue_usd" in body


@pytest.mark.parametrize(
    "dwell_days,free_days,expected_overdue,tier_1,tier_2",
    [
        (13, 5, 8, 5, 3),
        (5, 5, 0, 0, 0),
        (10, 5, 5, 5, 0),
    ],
)
def test_pure_dwell_and_tier_split_math(dwell_days, free_days, expected_overdue, tier_1, tier_2):
    assert calculate_overdue_days_count(dwell_days, free_days) == expected_overdue
    assert split_tier_overdue_days(expected_overdue) == (tier_1, tier_2)


def test_port_exception_overlap_engine():
    logs = [
        {
            "berth_terminal_name": "Jebel Ali Terminal T1",
            "exception_start_timestamp": "2026-09-11T08:00:00",
            "exception_end_timestamp": "2026-09-13T18:00:00",
        }
    ]
    assert verify_port_exception_overlap(
        "Jebel Ali Terminal T1",
        date(2026, 9, 9),
        date(2026, 9, 22),
        logs,
    )
    assert not verify_port_exception_overlap(
        "Jebel Ali Terminal T2",
        date(2026, 9, 9),
        date(2026, 9, 22),
        logs,
    )


def test_auto_waiver_decision_state_machine():
    assert evaluate_dispute_claim_decision(300.0, True) == ("AUTO_APPROVED", 300.0)
    assert evaluate_dispute_claim_decision(750.0, True) == ("ESCALATED_TO_MANAGER", 0.0)
    assert evaluate_dispute_claim_decision(200.0, False) == ("REJECTED", 0.0)
