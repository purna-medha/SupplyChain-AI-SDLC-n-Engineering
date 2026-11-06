"""Run the synthetic read-only API for examples 01 and 04. Stop with Ctrl+C.

Demo tokens are public classroom fixtures, not production authentication.
"""

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlsplit

records = {"C1": {"owner": "A", "fee": 100, "shipment_status": "delayed"},
           "C2": {"owner": "B", "fee": 200, "shipment_status": "on_time"}}
callers = {"Bearer demo-A": "A", "Bearer demo-B": "B"}


class ContainerAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path).path
        container_id = unquote(path.removeprefix("/containers/"))
        caller = callers.get(self.headers.get("Authorization"))
        record = records.get(container_id)
        if caller is None:
            code, body = 401, {"status": "unauthenticated"}
        elif not path.startswith("/containers/") or not re.fullmatch(r"C\d{1,6}", container_id):
            code, body = 400, {"status": "invalid_request"}
        elif record is None or record["owner"] != caller:
            code, body = 404, {"status": "unavailable"}
        else:
            code, body = 200, {"status": "ok", "container_id": container_id,
                               "shipment_status": record["shipment_status"], "fee": record["fee"],
                               "currency": "USD", "as_of": "2026-11-06T00:00:00Z",
                               "source": "training-api"}
        print("AUDIT:", {"caller": caller, "container_id": container_id, "http_status": code}, flush=True)
        encoded = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8766), ContainerAPI)
    print("Classroom API: http://127.0.0.1:8766/containers/C1", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
