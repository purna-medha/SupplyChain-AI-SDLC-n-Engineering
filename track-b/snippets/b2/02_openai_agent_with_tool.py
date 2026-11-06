"""Give the same agent one real Python function to obtain a recorded status.

Try: ask for C2, then C9. Watch the TOOL print before reading the answer.
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, set_default_openai_key, set_tracing_disabled

load_dotenv()
set_default_openai_key(os.environ["OPEN_AI_KEY"])
set_tracing_disabled(True)


@function_tool
def get_container_status(container_id: str) -> str:
    """Read a container's recorded status from the synthetic classroom records."""
    print("TOOL get_container_status:", container_id)
    records = {"C1": "delayed", "C2": "on_time"}
    return records.get(container_id, "Unknown container")

@function_tool
def get_status(id: str) -> str:
    print("TOOL get_status:", id)
    pass

@function_tool
def update_status(container_id: str) -> str:
    print("TOOL update_status:", container_id)
    pass

@function_tool
def get_update(id: str) -> str:
    print("TOOL get_status:", id)
    pass
agent = Agent(
    name="Port operations assistant",
    instructions="Get me the current latest update. Don't update any status",
    model="gpt-6-sol",
    tools=[get_container_status, get_status, get_update, update_status],
)

result = Runner.run_sync(agent, "Get me the current latest update on port P1 \
    and container C2. Update the status update of container C2", max_turns=40)
print(result.final_output)
