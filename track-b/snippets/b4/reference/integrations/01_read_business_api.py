"""Read an actual local HTTP API. First run service.py in another terminal.

Try: request C2 or C9, change the demo token, then stop the server and repeat.
"""

import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

container_id = "C1"
request = Request(
    "http://127.0.0.1:8766/containers/" + quote(container_id, safe=""),
    headers={"Authorization": "Bearer demo-A"},  # Trusted host credential fixture.
)
try:
    with urlopen(request, timeout=2) as response:
        record = json.load(response)
    print("RECORDED FACT:", record)
except HTTPError as error:
    print("UNAVAILABLE" if error.code == 404 else "HTTP ERROR", error.code)
except (URLError, TimeoutError) as error:
    print("SERVICE UNAVAILABLE:", type(error).__name__)
# A valid ID is not proof of access. The service enforces the caller's scope.
