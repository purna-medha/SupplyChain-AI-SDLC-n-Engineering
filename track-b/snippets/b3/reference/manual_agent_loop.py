"""Repeat a model/tool exchange while returning each observation to the model.

Try: reduce max_turns to one and inspect the stop reason.
"""

import json
import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_c1",
            "description": "Read C1's recorded status.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    }
]
messages = [{"role": "user", "content": "Read C1, then explain its status."}]
max_turns = 3
for turn in range(max_turns):
    response = completion(
        model="openai/gpt-4.1-mini",
        api_key=os.environ["OPENAI_API_KEY"],
        messages=messages,
        tools=tools,
        tool_choice="auto",
        timeout=20,
        num_retries=1,
    )
    message = response.choices[0].message
    messages.append(message.model_dump(exclude_none=True))
    if not message.tool_calls:
        print("FINAL:", message.content)
        break
    for call in message.tool_calls:
        print("REQUEST:", call.function.name, call.function.arguments)
        try:
            if (
                call.function.name != "read_c1"
                or json.loads(call.function.arguments) != {}
            ):
                raise ValueError("Unknown operation or unexpected arguments")
            observation = {"container_id": "C1", "status": "delayed"}
        except (ValueError, TypeError) as error:
            observation = {"error": str(error)}
        print("OBSERVATION:", observation)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(observation),
            }
        )
else:
    print("STOP: model-turn budget exhausted")
# num_retries bounds SDK retries per turn; max_turns bounds the outer loop.
