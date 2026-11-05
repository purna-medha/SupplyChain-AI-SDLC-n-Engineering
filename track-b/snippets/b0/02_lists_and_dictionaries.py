"""Represent one record, then a collection. Try: append another container."""

container = {"container_id": "C1", "status": "delayed"}
print("Identifier:", container["container_id"])
print("Missing departure:", container.get("scheduled_departure"))

containers = [container, {"container_id": "C2", "status": "on_time"}]
print("First record:", containers[0])
print("Number of records:", len(containers))

