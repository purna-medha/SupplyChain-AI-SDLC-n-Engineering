"""Select work from each record. Try: change C2's recorded status."""

containers = [
    {"container_id": "C1", "status": "delayed"},
    {"container_id": "C2", "status": "on_time"},
    {"container_id": "C9", "status": "unknown"},
]

for container in containers:
    if container["status"] == "delayed":
        next_step = "investigate"
    elif container["status"] == "on_time":
        next_step = "finish"
    else:
        next_step = "clarify"
    print(container["container_id"], "->", next_step)

