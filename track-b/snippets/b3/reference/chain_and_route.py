"""Grow a fixed chain into a workflow with an explicit route and state.

Try: change C1 to on_time and inspect which steps are skipped.
"""

records = {"C1": "delayed", "C2": "on_time"}


def read(container_id):
    print("READ", container_id)
    return {"container_id": container_id, "status": records[container_id]}


def draft(state):
    print("DRAFT", state["container_id"])
    return {**state, "text": f"{state['container_id']} is {state['status']}."}


print("Fixed chain:", draft(read("C1")))

state = read("C2")
if state["status"] == "delayed":
    state = draft(state)
    state["next"] = "human_review"
elif state["status"] == "on_time":
    state["next"] = "done"
else:
    state["next"] = "manual_check"
print("Routed workflow:", state)
