"""PortOps dual-persona dashboard — HTTP-only, no direct database access."""

import streamlit as st

from ui.api_http_client import SupplyChainOpsApiClient

st.set_page_config(page_title="PortOps — SupplyChainOps", layout="wide")
st.title("PortOps — Jebel Ali Container Terminal")

api_base_url = st.sidebar.text_input("API Base URL", value="http://localhost:8002")
client = SupplyChainOpsApiClient(api_base_url)

try:
    health = client.health_check()
    st.sidebar.success(f"{health['application_name']} — {health['status']}")
except Exception as exc:
    st.sidebar.error(f"API unreachable: {exc}")
    st.stop()

importer_tab, port_ops_tab = st.tabs(
    ["Importer & Cargo Owner Portal", "Port Operations & Logistics Workspace"]
)

with importer_tab:
    st.header("Importer & Cargo Owner Portal")
    importers = client.list_importers()
    importer_options = {
        row["importer_company_name"]: row["importer_identifier"] for row in importers
    }
    selected_importer_name = st.selectbox(
        "Select Importer Company",
        options=list(importer_options.keys()),
    )
    importer_identifier = importer_options[selected_importer_name]
    status_filter = st.selectbox(
        "Container Status Filter",
        options=["ALL", "IN_TERMINAL", "OVERDUE", "GATED_OUT"],
    )
    filter_value = None if status_filter == "ALL" else status_filter
    containers = client.list_containers(importer_identifier, filter_value)

    if not containers:
        st.info("No containers match the selected filters.")
    else:
        st.dataframe(containers, use_container_width=True)
        container_ids = [row["container_identifier"] for row in containers]
        selected_container = st.selectbox("Inspect Container", container_ids)
        demurrage = client.get_demurrage_calculation(selected_container)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Dwell Days", demurrage["container_dwell_days"])
        col2.metric("Overdue Days", demurrage["overdue_days_count"])
        col3.metric("Gross Fee (USD)", f"${demurrage['gross_demurrage_fee_usd']:,.2f}")
        col4.metric("Net Payable (USD)", f"${demurrage['net_payable_demurrage_fee_usd']:,.2f}")
        if demurrage.get("approved_waiver_amount_usd", 0) > 0:
            st.info(f"Approved waiver: ${demurrage['approved_waiver_amount_usd']:,.2f}")

        st.subheader("Submit Dispute Claim")
        with st.form("dispute_claim_form"):
            disputed_amount = st.number_input("Disputed Amount (USD)", min_value=0.01, value=250.0)
            dispute_reason = st.selectbox(
                "Dispute Reason Category",
                ["CRANE_BREAKDOWN", "CUSTOMS_SERVER_OUTAGE", "WEATHER_HOLD"],
            )
            submitted = st.form_submit_button("Submit Claim")
            if submitted:
                claim = client.submit_dispute_claim(
                    {
                        "container_identifier": selected_container,
                        "importer_identifier": importer_identifier,
                        "disputed_amount_usd": disputed_amount,
                        "dispute_reason_category": dispute_reason,
                    }
                )
                st.success(
                    f"Claim #{claim['dispute_claim_identifier']} — "
                    f"{claim['claim_decision_status']} "
                    f"(Waiver: ${claim['approved_waiver_amount_usd']:,.2f})"
                )

        if st.button("Execute Gate Out", key="importer_gate_out"):
            result = client.execute_gate_out(selected_container)
            st.success(f"Gated out on {result['gate_out_date']}")

with port_ops_tab:
    st.header("Port Operations & Logistics Workspace")
    summary = client.get_operational_summary()
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Gross Accrued Fees", f"${summary['gross_accrued_demurrage_fees_usd']:,.2f}")
    m2.metric("Approved Waivers", f"${summary['approved_credit_waivers_usd']:,.2f}")
    m3.metric("Net Revenue", f"${summary['net_demurrage_revenue_usd']:,.2f}")
    m4.metric("At-Risk Containers", summary["at_risk_container_count"])
    m5.metric("Escalated Claims", summary["pending_escalated_claim_count"])

    st.subheader("Dispute Claims Audit")
    claim_filter = st.selectbox(
        "Filter by Decision Status",
        ["ALL", "AUTO_APPROVED", "ESCALATED_TO_MANAGER", "REJECTED"],
    )
    claims = client.list_dispute_claims(
        None if claim_filter == "ALL" else claim_filter
    )
    st.dataframe(claims, use_container_width=True)

    escalated = [row for row in claims if row["claim_decision_status"] == "ESCALATED_TO_MANAGER"]
    if escalated:
        st.subheader("Manager Waiver Override")
        claim_options = {
            f"Claim #{row['dispute_claim_identifier']} — {row['container_identifier']}": row
            for row in escalated
        }
        selected_claim_label = st.selectbox("Escalated Claim", list(claim_options.keys()))
        selected_claim = claim_options[selected_claim_label]
        with st.form("manager_override_form"):
            waiver_amount = st.number_input(
                "Approved Waiver Amount (USD)",
                min_value=0.0,
                max_value=float(selected_claim["disputed_amount_usd"]),
                value=float(selected_claim["disputed_amount_usd"]),
            )
            override_note = st.text_input("Manager Override Note", value="Approved after review")
            override_submitted = st.form_submit_button("Approve Override")
            if override_submitted:
                updated = client.approve_claim_override(
                    selected_claim["dispute_claim_identifier"],
                    waiver_amount,
                    override_note,
                )
                st.success(f"Claim updated — waiver ${updated['approved_waiver_amount_usd']:,.2f}")

    st.subheader("Drayage Dispatch Jobs")
    drivers = sorted(
        {row["assigned_truck_driver_name"] for row in client.list_drayage_jobs()}
    )
    driver_filter = st.selectbox("Filter by Driver", ["ALL"] + drivers)
    drayage_jobs = client.list_drayage_jobs(
        None if driver_filter == "ALL" else driver_filter
    )
    st.dataframe(drayage_jobs, use_container_width=True)
