### Executive Summary

**SupplyChainOps** serves as an enterprise digital twin uniting maritime import terminal operations (**PortOps**) and inland drayage trucking dispatch (**FleetOps**) into a single operational system. Modeled on container shipping workflows at major global maritime hubs like Jebel Ali Port (DP World / Maersk), the platform connects ocean import logistics, container dwell time tracking, step-tariff demurrage penalty math, automated dispute waiver processing, and warehouse transport SLA monitoring across cargo importers, terminal operators, and drayage dispatchers.

---

### Core Business Problem & Industry Context

When ocean cargo containers arrive at a port berth, importers receive a fixed "Free Time" window (typically 5 days) to clear customs and retrieve their cargo. Containers sitting past this free allowance incur heavy daily penalty fees called **Demurrage & Detention (D&D)**, ranging from $150 to $300 per day.

This environment creates three major operational friction points:

* **Unearned Penalty Inflation:** Importers absorb millions in accrued demurrage fees caused by delays outside their control.


* **Dispute Friction:** 20% to 30% of demurrage fees are disputed because delays are frequently port-side bottlenecks (e.g., terminal crane breakdowns, customs system crashes, or weather holds) rather than importer negligence. Manually cross-examining claim narratives against port logs is slow and labor-intensive.


* **Inland Delivery Disconnect:** Once a container gates out of the port, lack of visibility into inland drayage truck dispatching causes transit route SLA breaches and warehouse receiving delays.



---

### Dual Operational User Views

The application coordinates two distinct business roles over a shared operational dataset:

#### 1. Importer & Freight Forwarder Portal (Customer View)

* **Active Container Tracking:** Allows importers (e.g., Al-Futtaim Logistics) to view live container discharge dates, remaining free-day allowances, and current dwell status.


* **Real-Time Fee Transparency:** Displays live calculated gross demurrage fees itemized by cargo type and fee rate tiers.


* **Dispute Claim Submission:** Enables importers to submit formal dispute claims for delay exceptions (e.g., claiming a 2-day terminal crane outage) and receive instant resolution updates.



#### 2. Port Operations & Logistics Workspace (Internal View)

* **Macro Revenue & Risk Dashboard:** Enables port managers to monitor top-level KPIs including Gross Accrued Demurrage, Approved Credit Waivers, Net Receivable Revenue, and At-Risk Containers nearing free-time expiry.


* **Dispute Audit Queue:** Provides finance teams with a workspace to cross-examine claims against immutable port exception logs and execute manual credit waiver overrides.


* **Fleet Drayage Dispatching:** Coordinates truck assignments from port gates to destination warehouses, tracking driver assignments and delivery SLA target hours.



---

### Key Business Rules & Deterministic Logic

* **Container Dwell & Overdue Tracking:** Computes dwell days as the difference between the Gate-Out Date (or current date) and the Vessel Discharge Date. Overdue days accumulate once dwell time exceeds the carrier's granted free days.


* **Tiered Step-Tariff Penalty Math:** Applies escalating daily penalty rates on overdue days (e.g., Days 1–5 overdue = $150/day; Days 6+ overdue = $300/day). Gross fees are adjusted based on the importer's commercial tier discount (Standard: 0%, Gold: 10%, Platinum: 20%).


* **Automated Dispute State Machine:**
* **Auto-Approved:** If the dispute reason matches a recorded entry in immutable terminal exception logs during the container's dwell period **AND** the disputed amount is under $500.00, a 100% credit waiver is automatically issued.


* **Escalated to Manager:** If a matching port outage log exists but the disputed amount is $\ge \$500.00$, the claim is routed to the manager approval queue.


* **Rejected:** If no matching port exception log is found, the claim is rejected ($0.00 waiver).




* **Drayage Transit SLA Penalty:** Calculates financial penalties at $50.00 per hour for actual inland transit times that exceed agreed SLA target delivery windows.



---

### Business Value & Strategic Impact

* **Eliminates Unearned Penalties:** Automates verification of port-side outages, ensuring importers are only penalized for genuine delays.


* **Accelerates Dispute Resolution:** Replaces manual email back-and-forth by auto-resolving up to 80% of routine cargo claims under preset financial thresholds.


* **Synchronizes Logistics Operations:** Bridges ocean gate-out events directly with inland trucking dispatch, reducing warehouse receiving delays and protecting transit SLAs.