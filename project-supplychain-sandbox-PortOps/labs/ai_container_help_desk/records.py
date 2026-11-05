"""Supplied PortOps HTTP adapter. Use existing services; do not recreate tariff math.

The configured importer is a classroom scope, not authenticated user identity.
No database imports or write endpoints are used by this lab.
"""

import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import urlopen

from dotenv import load_dotenv

LAB = Path(__file__).resolve().parent
for directory in (LAB, LAB.parents[1], LAB.parents[2]):
    load_dotenv(directory / ".env")

DEFAULT_CONTAINER = "MSKU1234567"
MCP_PORT = 8872
BASE_URL = os.environ.get("PORTOPS_URL", "http://127.0.0.1:8002").rstrip("/")
IMPORTER = os.environ.get("PORTOPS_IMPORTER", "IMP-GULF-001")
SOURCE = f"PortOps GET API at {BASE_URL}; importer scope {IMPORTER}; fees as of the server calculation date."


def get_json(path):
    print("HTTP GET:", path, flush=True)
    try:
        with urlopen(BASE_URL + path, timeout=10) as response:
            return json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"PortOps returned HTTP {exc.code} for {path}; inspect the API, do not invent a record.") from exc
    except URLError as exc:
        raise RuntimeError(f"PortOps is unavailable at {BASE_URL}. Start its API on port 8002.") from exc


def get_container(container_id):
    rows = get_json("/containers?" + urlencode({"importer_identifier": IMPORTER}))
    return next((row for row in rows if row["container_identifier"] == container_id), None)


def get_demurrage(container_id):
    # The fee endpoint itself has no importer argument. Check the scoped list FIRST.
    if get_container(container_id) is None:
        return None
    identifier = quote(container_id, safe="")
    return get_json(f"/containers/{identifier}/demurrage-calculation")


if __name__ == "__main__":
    print(SOURCE)
    print("HEALTH:", get_json("/health"))
    for identifier in [DEFAULT_CONTAINER, "MSCU7654321", "C9"]:
        print("CONTAINER:", get_container(identifier))
        print("DEMURRAGE:", get_demurrage(identifier))
