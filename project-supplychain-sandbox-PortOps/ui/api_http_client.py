"""HTTP client wrapper — Streamlit must not import database modules."""

from typing import Any, Dict, List, Optional

import requests

DEFAULT_BASE_URL = "http://localhost:8002"


class SupplyChainOpsApiClient:
    def __init__(self, base_url: str = DEFAULT_BASE_URL):
        self.base_url = base_url.rstrip("/")

    def _get(self, path: str, params: Optional[Dict] = None) -> Any:
        response = requests.get(f"{self.base_url}{path}", params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, payload: Optional[Dict] = None) -> Any:
        response = requests.post(f"{self.base_url}{path}", json=payload or {}, timeout=10)
        response.raise_for_status()
        return response.json()

    def _put(self, path: str, payload: Dict) -> Any:
        response = requests.put(f"{self.base_url}{path}", json=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    def health_check(self) -> Dict:
        return self._get("/health")

    def list_importers(self) -> List[Dict]:
        return self._get("/importers")

    def list_containers(
        self,
        importer_identifier: str,
        status_filter: Optional[str] = None,
    ) -> List[Dict]:
        params: Dict[str, str] = {"importer_identifier": importer_identifier}
        if status_filter:
            params["status_filter"] = status_filter
        return self._get("/containers", params=params)

    def get_demurrage_calculation(self, container_identifier: str) -> Dict:
        return self._get(f"/containers/{container_identifier}/demurrage-calculation")

    def execute_gate_out(self, container_identifier: str) -> Dict:
        return self._post(f"/containers/{container_identifier}/gate-out-execution")

    def submit_dispute_claim(self, payload: Dict) -> Dict:
        return self._post("/dispute-claims/submit", payload)

    def list_dispute_claims(
        self,
        claim_decision_status_filter: Optional[str] = None,
    ) -> List[Dict]:
        params = {}
        if claim_decision_status_filter:
            params["claim_decision_status_filter"] = claim_decision_status_filter
        return self._get("/dispute-claims", params=params or None)

    def approve_claim_override(
        self,
        dispute_claim_identifier: int,
        approved_waiver_amount_usd: float,
        manager_override_note: str,
    ) -> Dict:
        return self._put(
            f"/dispute-claims/{dispute_claim_identifier}/approve-override",
            {
                "approved_waiver_amount_usd": approved_waiver_amount_usd,
                "manager_override_note": manager_override_note,
            },
        )

    def list_drayage_jobs(
        self,
        assigned_driver_name_filter: Optional[str] = None,
    ) -> List[Dict]:
        params = {}
        if assigned_driver_name_filter:
            params["assigned_driver_name_filter"] = assigned_driver_name_filter
        return self._get("/drayage-dispatch-jobs", params=params or None)

    def get_operational_summary(self) -> Dict:
        return self._get("/analytics/operational-summary")
