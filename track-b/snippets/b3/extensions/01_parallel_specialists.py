"""Run independent model tasks concurrently, then aggregate their outcomes.

The supplied facts are synthetic inputs. No live shipment lookup occurs here.
"""

import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, set_default_openai_key, set_tracing_disabled

load_dotenv()
set_default_openai_key(os.environ["OPEN_AI_KEY"])
set_tracing_disabled(True)
operations = Agent(name="Operations", model="gpt-4.1-mini",
                   instructions="Summarize only the supplied operational facts in one sentence.")
charges = Agent(
    name="Charges", model="gpt-4.1-mini",
    instructions=("Summarize only the supplied shipment-charge facts in one sentence. "
                  "Preserve the classroom policy label and do not infer additional facts."),
)


async def run_specialist(name, agent, facts):
    print("START", name, flush=True)
    result = await Runner.run(agent, facts, max_turns=2)
    print("COMPLETED", name, flush=True)
    return result.final_output


async def main():
    names = ["operations", "charges"]
    results = await asyncio.gather(
        run_specialist("operations", operations,
                       "Synthetic classroom shipment C1: delayed by customs hold."),
        run_specialist("charges", charges,
                       "Classroom shipment C1: 2 delay days, 1 free day, USD 100 per "
                       "chargeable day. Deterministic result: (2 - 1) * 100 = USD 100 "
                       "exposure. This teaching rule is illustrative, not a real invoice."),
        return_exceptions=True,
    )
    for name, result in zip(names, results):
        print(name, "ERROR" if isinstance(result, Exception) else "RESULT", result)
    complete = all(not isinstance(result, Exception) for result in results)
    print("AGGREGATE:", "complete" if complete else "partial")


asyncio.run(main())
