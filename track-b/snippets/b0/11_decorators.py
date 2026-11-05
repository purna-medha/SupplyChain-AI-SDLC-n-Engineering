"""Wrap an ordinary function. Try: inspect the print before its result."""


def announce(function):
    def wrapped(container_id):
        print("Calling:", function.__name__, container_id)
        return function(container_id)
    return wrapped


@announce
def get_status(container_id: str) -> str:
    records = {"C1": "delayed", "C2": "on_time"}
    return records.get(container_id, "unknown")


print("Observation:", get_status("C1"))

