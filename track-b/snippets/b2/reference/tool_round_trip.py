"""Receive a tool request, validate it, execute it and return its observation.

Try: ask for C2; the trusted caller scope permits only C1.
"""

import json
import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
records = {"C1": "delayed", "C2": "on_time"}
allowed_ids = {"C1"}  # Trusted classroom caller fixture.
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_status",
            "description": "Read a recorded container status.",
            "parameters": {
                "type": "object",
                "properties": {"container_id": {"type": "string"}},
                "required": ["container_id"],
                "additionalProperties": False,
            },
        },
    }
]
messages = [{"role": "user", "content": "Read C1's recorded status."}]
first = completion(
    model="openai/gpt-4.1-mini",
    api_key=os.environ["OPENAI_API_KEY"],
    messages=messages,
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "get_status"}},
)
message = first.choices[0].message
messages.append(message.model_dump(exclude_none=True))
if not message.tool_calls:
    raise RuntimeError("No tool request returned")
for call in message.tool_calls:
    print("Proposed:", call.function.name, call.function.arguments)
    args = json.loads(call.function.arguments)
    if (
        call.function.name != "get_status"
        or not isinstance(args, dict)
        or set(args) != {"container_id"}
        or not isinstance(args["container_id"], str)
        or args["container_id"] not in allowed_ids
        or args["container_id"] not in records
    ):
        raise ValueError("Rejected before reading the record")
    observation = {
        "container_id": args["container_id"],
        "status": records[args["container_id"]],
    }
    print("Executed read:", observation)
    messages.append(
        {"role": "tool", "tool_call_id": call.id, "content": json.dumps(observation)}
    )
final = completion(
    model="openai/gpt-4.1-mini",
    api_key=os.environ["OPENAI_API_KEY"],
    messages=messages,
    tools=tools,
    tool_choice="none",
)
print("Answer:", final.choices[0].message.content)
