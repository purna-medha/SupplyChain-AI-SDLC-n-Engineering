"""B3 starter: investigate a container enquiry, retain a draft, review an action.

Core: route -> investigate -> follow-up -> review. Two optional delegation modes.
The supplied tools are complete, so unfinished B2 functions cannot block B3.
"""

import argparse
import asyncio
import json
from pathlib import Path
from uuid import uuid4

from agents import Agent, MaxTurnsExceeded, Runner, RunState, SQLiteSession, function_tool

from records import DEFAULT_CONTAINER, SOURCE, get_container, get_demurrage
from support import WORK, append_outbox, configure_sdk, load_task, run_cli, task_path


# Learner work: keep these functions small. Contracts and source examples are in B3.md.
def choose_route(status: str) -> str:
    """B3.1: OVERDUE -> investigate; known other status -> finish; unknown -> clarify."""
    # TODO: handle IN_TERMINAL/GATED_OUT explicitly; unfamiliar labels -> review.
    raise NotImplementedError("TODO B3.1: implement choose_route")


def make_investigator() -> Agent:
    """B3.2: one agent chooses among the supplied planning and read tools."""
    # TODO: Agent with record_plan, read_status and read_fee; max turns is in the runner.
    # Instruct it to read status first, investigate overdue fees, clarify unknown IDs,
    # and return a short factual draft for review. No sending or claims of approval.
    raise NotImplementedError("TODO B3.2: implement make_investigator")


def save_task(state: dict, path: Path) -> None:
    """B3.3: save application-owned findings, actual draft and review status as JSON."""
    # TODO: write json.dumps(state, indent=2) using path.write_text(..., encoding="utf-8").
    raise NotImplementedError("TODO B3.3: implement save_task")


def make_review_agent() -> Agent:
    """B3.4: give a separate agent only the supplied approval-gated outbox tool."""
    # TODO: register queue_customer_update, which already has needs_approval=True.
    # Ask for the supplied exact payload unchanged; a rejected action must not be retried.
    raise NotImplementedError("TODO B3.4: implement make_review_agent")


def review_pending(saved: RunState, decision: str) -> None:
    """B3.5: validate the human input, then approve or reject the pending calls."""
    # TODO: accept only "approve" or "reject"; otherwise raise ValueError before changing state.
    # For each saved.get_interruptions(), call saved.approve(item) or saved.reject(item).
    raise NotImplementedError("TODO B3.5: implement review_pending")


def make_coordinator(operations: Agent, charges: Agent) -> Agent:
    """Extension B3.X1: specialists are tools; the coordinator owns the final reply."""
    # TODO: expose each specialist with .as_tool(..., max_turns=4); register both tools.
    raise NotImplementedError("TODO B3.X1: implement make_coordinator (optional)")


def make_triage(operations: Agent, charges: Agent) -> Agent:
    """Extension B3.X2: hand off so the appropriate specialist owns the final reply."""
    # TODO: use handoffs=[operations, charges] and instructions to choose the relevant owner.
    raise NotImplementedError("TODO B3.X2: implement make_triage (optional)")


# Supplied application tools: observations populate task state as well as model context.
findings = []
review_task = None
review_action_executed = False


@function_tool
def record_plan(steps: list[str]) -> str:
    """Print a brief proposed task checklist; it is not evidence of execution."""
    print("PLAN:", steps, flush=True)
    return "Plan recorded; use read tools for evidence."


@function_tool(failure_error_function=None)
def read_status(container_id: str) -> dict:
    """Read status and dwell from the configured source; absence means unknown."""
    row = get_container(container_id)
    observation = {"container_id": container_id, "source": SOURCE,
                   "status": row["container_status_label"] if row else "unknown",
                   "record": row}
    findings.append(observation)
    print("OBSERVATION:", observation, flush=True)
    return observation


@function_tool(failure_error_function=None)
def read_fee(container_id: str) -> dict:
    """Read the source's calculated demurrage; never invent rates or recompute it."""
    observation = {"container_id": container_id, "source": SOURCE,
                   "demurrage": get_demurrage(container_id)}
    findings.append(observation)
    print("OBSERVATION:", observation, flush=True)
    return observation


@function_tool(needs_approval=True, failure_error_function=None)
def queue_customer_update(container_id: str, text: str) -> str:
    """Save the reviewed draft in a local lab outbox; this sends no message."""
    global review_action_executed
    if review_task is None or container_id != review_task["container_id"] or text != review_task["draft"]:
        raise ValueError("The proposed payload differs from the saved draft; review the draft again.")
    append_outbox({"container_id": container_id, "text": text})
    review_action_executed = True
    print("ACTION: saved exact payload to", WORK / "outbox.jsonl", flush=True)
    return "Saved to the local lab outbox. No customer message was sent."


def conversation(container_id, new=False):
    WORK.mkdir(parents=True, exist_ok=True)
    session_id = f"desk-{container_id}" + (f"-empty-{uuid4().hex}" if new else "")
    return SQLiteSession(session_id, db_path=WORK / "conversation.db")


def specialists():
    operations = Agent(
        name="Operations specialist", model="gpt-4.1-mini",
        handoff_description="Answers container status and dwell questions.",
        instructions="Use read_status. Report observed status/dwell and missing facts.",
        tools=[read_status],
    )
    charges = Agent(
        name="Charges specialist", model="gpt-4.1-mini",
        handoff_description="Answers calculated demurrage and waiver questions.",
        instructions="Use read_fee. Preserve USD, net/gross distinctions and missing facts.",
        tools=[read_fee],
    )
    return operations, charges


async def run_review(container_id):
    global review_task, review_action_executed
    review_action_executed = False
    review_task = load_task(container_id)
    if review_task["review"] != "pending":
        raise ValueError("This draft already has a review outcome. Investigate again to prepare a new draft.")
    agent = make_review_agent()
    configure_sdk()
    payload = {"container_id": container_id, "text": review_task["draft"]}
    result = await Runner.run(agent, "Queue this exact payload: " + json.dumps(payload), max_turns=4)
    if not result.interruptions:
        raise ValueError("No pending action was produced. Nothing has been approved; inspect the run.")
    for item in result.interruptions:
        print("PENDING:", item.name, item.arguments)
        if item.name != "queue_customer_update" or json.loads(item.arguments) != payload:
            raise ValueError("Pending action differs from the saved payload. Stopped before approval.")
    path = WORK / f"pending-{container_id}.json"
    path.write_text(json.dumps(result.to_state().to_json()), encoding="utf-8")
    saved = await RunState.from_json(agent, json.loads(path.read_text(encoding="utf-8")))
    print("RESTORED PENDING RUN:", path)
    print("No outbox tool body has run in this review yet.")
    decision = input("Review the exact PENDING payload. Type approve or reject: ").strip().lower()
    review_pending(saved, decision)
    resumed = await Runner.run(agent, saved, max_turns=4)
    if resumed.interruptions:
        raise ValueError("Another proposal needs its own review. Stopped without approving it.")
    review_task["review"] = "rejected" if decision == "reject" else "queued" if review_action_executed else "incomplete"
    save_task(review_task, task_path(container_id))
    print("REVIEW OUTCOME:", review_task["review"])
    print("AGENT REPLY:", resumed.final_output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", nargs="?", choices=["route", "investigate", "follow-up", "review", "specialists", "handoff"])
    parser.add_argument("--container", default=DEFAULT_CONTAINER)
    parser.add_argument("--max-turns", type=int, default=8)
    parser.add_argument("--new-session", action="store_true")
    parser.add_argument("--question")
    args = parser.parse_args()
    if args.checkpoint is None:
        parser.print_help()
        return
    if args.max_turns < 1:
        raise ValueError("max-turns must be at least 1.")
    task_path(args.container)  # Validate before using this identifier in any filename.
    if args.checkpoint == "route":
        row = get_container(args.container)
        print("ROUTE:", choose_route(row["container_status_label"] if row else "unknown"))
        return
    if args.checkpoint == "review":
        asyncio.run(run_review(args.container))
        return
    if args.checkpoint in {"specialists", "handoff"}:
        operations, charges = specialists()
        agent = make_coordinator(operations, charges) if args.checkpoint == "specialists" else make_triage(operations, charges)
        question = args.question or f"Explain {args.container}'s net demurrage in USD."
        configure_sdk()
        result = Runner.run_sync(agent, question, max_turns=args.max_turns)
        print("FINAL OWNER:", result.last_agent.name)
        print("ANSWER:", result.final_output)
        return
    agent = make_investigator()
    configure_sdk()
    if args.checkpoint == "follow-up":
        load_task(args.container)
        result = Runner.run_sync(
            agent, "Which container were we discussing? Reply with the identifier only; do not look it up.",
            session=conversation(args.container, args.new_session), max_turns=args.max_turns,
        )
        print("FOLLOW-UP:", result.final_output)
        return
    findings.clear()
    result = Runner.run_sync(
        agent, f"Investigate {args.container}'s dwell status and fees. Draft a short update for review.",
        session=conversation(args.container), max_turns=args.max_turns,
    )
    if not isinstance(result.final_output, str) or not result.final_output.strip():
        raise ValueError("No usable draft was produced.")
    state = {"container_id": args.container, "findings": list(findings),
             "draft": result.final_output, "review": "pending"}
    save_task(state, task_path(args.container))
    print("DRAFT:", state["draft"])
    print("SAVED:", task_path(args.container), "REVIEW:", state["review"])


if __name__ == "__main__":
    def run():
        try:
            main()
        except MaxTurnsExceeded:
            raise RuntimeError("Turn limit reached. This run is incomplete; no new completed draft was saved.") from None

    run_cli(run)
