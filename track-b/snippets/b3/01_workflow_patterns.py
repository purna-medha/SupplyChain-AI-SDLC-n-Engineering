"""Compare a fixed sequence with a branch chosen by ordinary Python.

Try: change C2's status. Inspect the route and which reads execute.
"""

records = {"C1": "delayed", "C2": "on_time"}


def get_shipment_status(container_id):
    print("READ status:", container_id)
    return records.get(container_id)


def get_tracking_events(container_id):
    print("READ events:", container_id)
    return {"C1": "Customs hold; planned departure missed.",
            "C2": "Departed as planned."}.get(container_id)


print("FIXED SEQUENCE")
status = get_shipment_status("C2")
events = get_tracking_events("C2")
print("SCRIPTED RESULT:", status, events)

print("\nCONDITIONAL WORKFLOW")
for container_id in ["C1", "C2", "C9"]:
    status = get_shipment_status(container_id)
    if status is None:
        route = "clarify"
    elif status == "delayed":
        route = "investigate"
        print("Evidence:", get_tracking_events(container_id))
    elif status == "on_time":
        route = "finish"
    else:
        route = "review"
    print(f"{container_id} route: {route}")

# Both paths are prescribed application logic. No language model runs here.
