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
            "dispute_reason_category": "CUSTOMS_SERVER_OUTAGE",
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
    assert body["claim_decision_status"] == "MANAGER_APPROVED"
    assert body["manager_override_note"] == "Partial waiver approved by terminal manager"
    saved = client.get(
        "/dispute-claims", params={"claim_decision_status_filter": "MANAGER_APPROVED"}
    ).json()
    assert len(saved) == 1
    assert saved[0]["manager_override_note"] == body["manager_override_note"]


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


def test_duplicate_claim_does_not_issue_a_second_waiver(client):
    payload = {
        "container_identifier": "MSKU1234567",
        "importer_identifier": "IMP-GULF-001",
        "disputed_amount_usd": 300.0,
        "dispute_reason_category": "CRANE_BREAKDOWN",
    }
    assert client.post("/dispute-claims/submit", json=payload).status_code == 201
    payload["disputed_amount_usd"] = 350.0
    payload["dispute_reason_category"] = " crane_breakdown "
    assert client.post("/dispute-claims/submit", json=payload).status_code == 409
    fee = client.get("/containers/MSKU1234567/demurrage-calculation").json()
    assert fee["approved_waiver_amount_usd"] == 300.0
    assert fee["net_payable_demurrage_fee_usd"] == 1200.0


def test_separate_claim_reasons_are_allowed(client):
    for reason in ("CRANE_BREAKDOWN", "CUSTOMS_SERVER_OUTAGE"):
        response = client.post("/dispute-claims/submit", json={
            "container_identifier": "MSKU1234567",
            "importer_identifier": "IMP-GULF-001",
            "disputed_amount_usd": 100.0,
            "dispute_reason_category": reason,
        })
        assert response.status_code == 201
    fee = client.get("/containers/MSKU1234567/demurrage-calculation").json()
    assert fee["approved_waiver_amount_usd"] == 200.0


def test_demurrage_response_keeps_the_existing_slim_contract(client):
    body = client.get("/containers/MSKU1234567/demurrage-calculation").json()
    assert set(body) == {
        "container_identifier", "container_dwell_days", "overdue_days_count",
        "gross_demurrage_fee_usd", "approved_waiver_amount_usd",
        "net_payable_demurrage_fee_usd", "tier_discount_percentage",
    }


def test_workflows_use_an_explicit_calculation_date(engine):
    from sqlmodel import Session
    from supplychainops.port_demurrage_service import (
        build_operational_summary, calculate_container_demurrage, execute_gate_out,
    )
    from supplychainops.port_read_service import fetch_containers_for_importer

    with Session(engine) as session:
        calculation_date = date(2026, 9, 14)
        fee = calculate_container_demurrage(session, "MSKU1234567", calculation_date)
        assert fee["gross_demurrage_fee_usd"] == 0.0
        rows = fetch_containers_for_importer(
            session, "IMP-GULF-001", current_calculation_date=calculation_date
        )
        assert rows[0]["container_status_label"] == "IN_TERMINAL"
        summary = build_operational_summary(session, calculation_date)
        assert summary["at_risk_container_count"] == 0
        result = execute_gate_out(session, "MSKU1234567", calculation_date)
        assert result["gate_out_date"] == calculation_date
        later_fee = calculate_container_demurrage(session, "MSKU1234567", date(2026, 10, 1))
        assert later_fee["gross_demurrage_fee_usd"] == 0.0


def test_claim_evidence_uses_explicit_date(engine):
    from sqlmodel import Session
    from supplychainops.port_claims_service import submit_dispute_claim

    with Session(engine) as session:
        claim = submit_dispute_claim(
            session, "MSKU1234567", "IMP-GULF-001", 200.0, "CRANE_BREAKDOWN",
            current_calculation_date=date(2026, 9, 10),
        )
        assert claim.claim_decision_status == "REJECTED"


@pytest.mark.parametrize("amount,note", [(-1.0, "Reviewed"), (100.0, "   ")])
def test_manager_override_rejects_invalid_values_in_service(engine, amount, note):
    from sqlmodel import Session
    from supplychainops.database_models import Claim
    from supplychainops.port_claims_service import ClaimValidationError, approve_manager_override

    with Session(engine) as session:
        claim = Claim(
            container_identifier="MSKU1234567", importer_identifier="IMP-GULF-001",
            disputed_amount_usd=750.0, dispute_reason_category="CRANE_BREAKDOWN",
            claim_decision_status="ESCALATED_TO_MANAGER",
        )
        session.add(claim)
        session.commit()
        with pytest.raises(ClaimValidationError):
            approve_manager_override(session, claim.dispute_claim_identifier, amount, note)
        session.refresh(claim)
        assert claim.claim_decision_status == "ESCALATED_TO_MANAGER"
        assert claim.approved_waiver_amount_usd == 0.0


def test_reset_removes_legacy_tables_and_keeps_a_recoverable_backup(tmp_path, monkeypatch):
    import sqlite3
    from sqlmodel import Session, create_engine, select
    import scripts.reset_database as reset
    from supplychainops.database_models import Claim, Container

    database_path = tmp_path / "portops.db"
    with sqlite3.connect(database_path) as connection:
        connection.execute("CREATE TABLE carrier (name TEXT)")
        connection.execute("INSERT INTO carrier VALUES ('original data')")
        connection.execute("CREATE TABLE tariff (rate REAL)")
    test_engine = create_engine(f"sqlite:///{database_path}")
    monkeypatch.setattr(reset, "get_engine", lambda: test_engine)
    backup_path = reset.seed_database()
    assert backup_path is not None and backup_path.exists()
    with sqlite3.connect(backup_path) as connection:
        assert connection.execute("SELECT name FROM carrier").fetchone() == ("original data",)
    with sqlite3.connect(database_path) as connection:
        tables = {row[0] for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
    assert tables == {
        "vessel", "importer", "shipment", "container", "terminal_event",
        "port_exception_log", "claim", "drayage_job",
    }
    with Session(test_engine) as session:
        assert len(session.exec(select(Container)).all()) == 4
        assert session.get(Claim, 1).manager_override_note is None
    second_backup = reset.seed_database()
    assert second_backup != backup_path
    with Session(test_engine) as session:
        assert len(session.exec(select(Container)).all()) == 4
    test_engine.dispose()


def test_reset_leaves_existing_database_untouched_when_seeds_are_invalid(tmp_path, monkeypatch):
    import sqlite3
    from sqlmodel import create_engine
    import scripts.reset_database as reset

    database_path = tmp_path / "portops.db"
    with sqlite3.connect(database_path) as connection:
        connection.execute("CREATE TABLE marker (value TEXT)")
        connection.execute("INSERT INTO marker VALUES ('keep me')")
    invalid_seed = tmp_path / "invalid.csv"
    invalid_seed.write_text("importer_identifier\nIMP-INCOMPLETE\n")
    test_engine = create_engine(f"sqlite:///{database_path}")
    monkeypatch.setattr(reset, "get_engine", lambda: test_engine)
    monkeypatch.setattr(reset, "SEED_DIRECTORY", tmp_path)
    monkeypatch.setattr(reset, "SEED_FILE_ORDER", [("invalid.csv", reset.Importer)])
    with pytest.raises(ValueError):
        reset.seed_database()
    with sqlite3.connect(database_path) as connection:
        assert connection.execute("SELECT value FROM marker").fetchone() == ("keep me",)
    test_engine.dispose()
