"""Optional FastAPI bridge: expose a synthetic read over HTTP.

From track-b:
uv run --with fastapi --with uvicorn uvicorn server:app --app-dir snippets/b0/extensions --port 8003
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/containers/{container_id}")
def get_container(container_id: str) -> dict[str, str]:
    records = {"C1": "delayed", "C2": "on_time"}
    return {"container_id": container_id, "status": records.get(container_id, "unknown")}
