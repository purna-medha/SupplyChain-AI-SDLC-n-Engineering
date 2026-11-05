"""Describe a familiar Python function as a model-facing tool.

Try: change the function call, then inspect its advertised argument schema.
"""

import json

records = {"C1": "delayed", "C2": "on_time"}


def get_status(container_id):
    return {"container_id": container_id, "status": records[container_id]}


print("Ordinary function result:", get_status("C1"))
tool = {
    "type": "function",
    "function": {
        "name": "get_status",
        "description": "Read the recorded container status.",
        "parameters": {
            "type": "object",
            "properties": {"container_id": {"type": "string"}},
            "required": ["container_id"],
            "additionalProperties": False,
        },
    },
}
print("Model-facing description:", json.dumps(tool, indent=2))
