"""Read a synthetic record with ordinary Python, before adding a model or tool.

Try: call the same function with C2, then unknown C9.
"""


def get_container_status(container_id: str) -> str:
    """Read a container's recorded status from the synthetic classroom records."""
    records = {"C1": "delayed", "C2": "on_time"}
    return records.get(container_id, "Unknown container")


print(get_container_status("C1"))
