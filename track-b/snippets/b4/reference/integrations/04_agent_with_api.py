"""Keep the familiar SDK tool contract; replace dictionary access with HTTP.

First run service.py. Try: ask for C2 or C9, or stop the service before running.
"""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
from dotenv import load_dotenv
from agents import Agent, MaxTurnsExceeded, Runner, function_tool
from agents import set_default_openai_key, set_tracing_disabled

load_dotenv()
set_default_openai_key(os.environ["OPEN_AI_KEY"])
set_tracing_disabled(True)


@function_tool
def read_container(container_id: str) -> dict:
    """Read a permitted recorded container fact. Unavailable is not a zero fee."""
    request = Request("http://127.0.0.1:8766/containers/" + quote(container_id, safe=""),
                      headers={"Authorization": "Bearer demo-A"})
    try:
        with urlopen(request, timeout=2) as response:
            observation = json.load(response)
    except HTTPError as error:
        observation = {"status": "unavailable" if error.code == 404 else "error",
                       "http_status": error.code}
    except (URLError, TimeoutError, json.JSONDecodeError):
        observation = {"status": "service_unavailable"}
    print("TOOL:", container_id, "OBSERVATION:", observation)
    return observation


agent = Agent(
    name="Container assistant", model="gpt-4.1-mini", tools=[read_container],
    instructions=("Use read_container. Quote currency, source and the full as_of timestamp exactly. "
                  "On unavailable/error, state the limitation and stop. Never invent a fee."),
)
try:
    result = Runner.run_sync(agent, "Read C1's recorded fee and its source/time.", max_turns=4)
    print("ANSWER:", result.final_output)
except MaxTurnsExceeded:
    print("INCOMPLETE: turn limit reached.")
    raise
