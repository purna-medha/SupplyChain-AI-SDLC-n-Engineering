"""Express the charges handoff through LlamaIndex's AgentWorkflow.

Compare this real handoff with the OpenAI SDK example's final owner and tool call.
"""

import asyncio
import os
from dotenv import load_dotenv
from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent
from llama_index.llms.openai import OpenAI

load_dotenv()
llm = OpenAI(model="gpt-4.1-mini", api_key=os.environ["OPEN_AI_KEY"])


def read_charge_exposure(container_id: str) -> dict:
    """Read a synthetic calculation, not an actual invoice."""
    print("CHARGES TOOL:", container_id)
    if container_id != "C1":
        return {"error": "unknown shipment"}
    return {"usd": 100, "policy": "synthetic teaching rule"}


triage = FunctionAgent(
    name="Triage", description="Routes shipment questions.", llm=llm,
    system_prompt="Hand charge questions to Charges, which should answer the user.",
    can_handoff_to=["Charges"], streaming=False,
)
charges = FunctionAgent(
    name="Charges", description="Answers illustrative charge questions.", llm=llm,
    system_prompt="Use your tool before answering; label its USD amount illustrative.",
    tools=[read_charge_exposure], can_handoff_to=[], streaming=False,
)
workflow = AgentWorkflow(agents=[triage, charges], root_agent="Triage", timeout=60)


async def main():
    result = await workflow.run(user_msg="What is C1's charge exposure?", max_iterations=6)
    print("FINAL:", result)


asyncio.run(main())
