"""B5 starter: diagnose a fee-decision failure and compare one rule repair.

Four learner TODOs; actual source reads, SDK tracing and trial runners are supplied.
The B5 fixtures are independent: caller A owns C1/USD 100 and C2/USD 200.
"""

import argparse
import hashlib
import json
from pathlib import Path
from time import perf_counter

from agents import Agent, MaxTurnsExceeded, ModelSettings, Runner, function_tool
from agents import set_trace_processors, set_tracing_disabled
from agents.tracing import Span
from agents.tracing.processors import BatchTraceProcessor, ConsoleSpanExporter

from support import WORK, configure_sdk, run_cli

MODEL = "gpt-4.1-mini"
SOURCE = "synthetic-b5-fees-v1"
INSTRUCTION = (
    "Call read_fee for the requested ID. Report its decision unchanged. "
    "Your final answer must be exactly its one-word label: clear, review, unknown, "
    "denied, or unavailable. Add no other words or punctuation."
)


def make_cases() -> list[dict]:
    """B5.1: five independent policy cases: below, boundary, missing, denied, dependency."""
    # TODO: each dict has name, caller, container_id, unavailable, expected_fee,
    # expected_decision. At least USD 200 requires review; absence has fee None.
    raise NotImplementedError("TODO B5.1: implement make_cases")


def grade_observation(expected: dict, actual: dict) -> bool:
    """B5.2: check ID, exact fee/type and decision; do not grade prose clarity here."""
    # TODO: expected has container_id, fee, decision. Return a bool.
    # Require the fields; integer amounts must not accept text/bool values.
    # A missing amount is None, not zero. Ignore additional source metadata.
    raise NotImplementedError("TODO B5.2: implement grade_observation")


def candidate_decision(fee: int) -> str:
    """B5.3: implement the corrected classroom rule; baseline below remains unchanged."""
    # TODO: return review for fee >= 200, otherwise clear.
    raise NotImplementedError("TODO B5.3: implement candidate_decision")


def make_agent(read_tool) -> Agent:
    """B5.4: same agent/instruction/settings for baseline and candidate trials."""
    # TODO: Agent(name=..., model=MODEL, tools=[read_tool], instructions=INSTRUCTION,
    #             model_settings=ModelSettings(temperature=0)).
    raise NotImplementedError("TODO B5.4: implement make_agent")


# Supplied source and runners: inspect these when locating the first incorrect result.
def observe_fee(case, container_id, repaired=False):
    fee = {"C1":100, "C2":200}.get(container_id)
    if fee is None:
        decision = "unknown"
    elif case["caller"] != "A":
        fee, decision = None, "denied"
    elif case["unavailable"]:
        fee, decision = None, "unavailable"
    else:
        decision = candidate_decision(fee) if repaired else "review" if fee > 200 else "clear"
    return {"container_id":container_id, "fee":fee, "decision":decision, "source":SOURCE}


def expected_observation(case):
    return {"container_id":case["container_id"], "fee":case["expected_fee"],
            "decision":case["expected_decision"]}


def cases_for_run():
    cases = make_cases()
    if not cases or len({case["name"] for case in cases}) != len(cases):
        raise ValueError("Provide a nonempty case set with unique names.")
    for case in cases:
        for field in ["name","caller","container_id","unavailable","expected_fee","expected_decision"]:
            if field not in case:
                raise ValueError(f"Case is missing {field}.")
    return cases


def probe_grader():
    expected = {"container_id":"C2", "fee":200, "decision":"review"}
    probes = [
        ("known correct", dict(expected), True),
        ("wrong amount", dict(expected, fee=999), False),
        ("wrong ID", dict(expected, container_id="C1"), False),
        ("wrong decision", dict(expected, decision="clear"), False),
        ("text amount", dict(expected, fee="200"), False),
        ("boolean amount", dict(expected, fee=True), False),
        ("missing fee", {"container_id":"C2", "decision":"review"}, False),
    ]
    for name, actual, reference in probes:
        accepted = grade_observation(expected, actual)
        print("PROBE:", name, "EXPECTED:", reference, "ACCEPTED:", accepted)
        if type(accepted) is not bool or accepted != reference:
            raise RuntimeError(f"Grader defect: {name}. Inspect the checker before trusting its scores.")


def direct_cases(cases, repaired):
    results = []
    for case in cases:
        actual = observe_fee(case, case["container_id"], repaired)
        passed = grade_observation(expected_observation(case), actual)
        print(case["name"], "EXPECTED:", expected_observation(case), "ACTUAL:", actual,
              "PASS" if passed else "FAIL")
        results.append({"case":case["name"], "actual":actual, "passed":passed})
    print("DIRECT PASSES:", sum(row["passed"] for row in results), "/", len(results))
    return results


class ReadableSpans(ConsoleSpanExporter):
    def export(self, items):
        for item in items:
            if isinstance(item, Span):
                print("SPAN:", item.span_data.type, item.span_id, "parent:", item.parent_id)
                if item.span_data.type == "function":
                    print("  ARGUMENTS:", item.span_data.input)
                    print("  OBSERVATION:", item.span_data.output)


def run_trial(case, repaired, max_turns, trace=False):
    calls, observations = [], []  # Fresh application state for THIS independent trial.

    @function_tool(failure_error_function=None)
    def read_fee(container_id: str) -> dict:
        """Read the recorded fee and application decision for a synthetic container."""
        calls.append(container_id)
        observation = observe_fee(case, container_id, repaired)
        observations.append(observation)
        print("TOOL OBSERVATION:", observation)
        return observation

    agent = make_agent(read_fee)  # A new Agent and conversation for every trial.
    trial = {"answer":None, "observation":None, "calls":calls, "error":None,
             "repaired":repaired, "input_tokens":None, "output_tokens":None}
    processor = None
    started = perf_counter()
    try:
        configure_sdk()
        if trace:
            processor = BatchTraceProcessor(ReadableSpans())
            set_trace_processors([processor])  # Local export replaces hosted tracing.
            set_tracing_disabled(False)
        result = Runner.run_sync(agent, f"Check {case['container_id']}.", max_turns=max_turns)
        trial["answer"] = result.final_output.strip()
        usage = result.context_wrapper.usage
        trial["input_tokens"], trial["output_tokens"] = usage.input_tokens, usage.output_tokens
    except NotImplementedError:
        raise
    except Exception as error:
        trial["error"] = {"type":type(error).__name__, "message":str(error)}
        print("INCOMPLETE:" if isinstance(error, MaxTurnsExceeded) else "ERROR:", type(error).__name__)
    finally:
        trial["seconds"] = round(perf_counter()-started, 3)
        trial["observation"] = observations[-1] if observations else None
        if processor:
            processor.force_flush()
        set_tracing_disabled(True)
    return trial


def trial_passed(case, trial):
    # These supplied task checks are separate from the learner's field grader.
    if trial["error"] or not trial["observation"] or not trial["calls"]:
        return False
    return (trial["answer"] == case["expected_decision"]
            and all(cid == case["container_id"] for cid in trial["calls"])
            and grade_observation(expected_observation(case), trial["observation"]))


def repeat_cases(cases, repaired, repeats, max_turns):
    trials = []
    for case in cases:
        passed = 0
        for attempt in range(repeats):
            trial = run_trial(case, repaired, max_turns)
            trial.update(case=case["name"], attempt=attempt+1, passed=trial_passed(case,trial))
            passed += trial["passed"]
            trials.append(trial)  # Errors/stops are retained in the same denominator.
            print(case["name"], "ATTEMPT:", attempt+1, "ANSWER:", trial["answer"],
                  "ERROR:", trial["error"], "PASS" if trial["passed"] else "FAIL")
        print(case["name"], "SUCCESS FREQUENCY:", passed, "/", repeats)
    return trials


def save_report(filename, report):
    WORK.mkdir(parents=True, exist_ok=True)
    report.update(model=MODEL, instruction=INSTRUCTION,
                  code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    path = WORK / filename
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("EVIDENCE:", path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", nargs="?", choices=["probe","baseline","trace","compare","trials"])
    parser.add_argument("--container", choices=["C1","C2","C9"], default="C2")
    parser.add_argument("--repaired", action="store_true", help="Use candidate rule for trace")
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--max-turns", type=int, default=4)
    args = parser.parse_args()
    if args.checkpoint is None:
        parser.print_help()
        return
    if args.repeats < 1 or args.max_turns < 1:
        raise ValueError("Repeats and turn limit must be positive.")
    if args.checkpoint == "probe":
        probe_grader()
    elif args.checkpoint == "trace":
        fee, decision = {"C1":(100,"clear"), "C2":(200,"review"), "C9":(None,"unknown")}[args.container]
        case = {"name":"trace", "caller":"A", "container_id":args.container, "unavailable":False,
                "expected_fee":fee, "expected_decision":decision}
        if args.repaired:
            candidate_decision(200)  # Surface an unfinished rule before any model call.
        trial = run_trial(case, args.repaired, args.max_turns, trace=True)
        print("EXPECTED:", expected_observation(case), "ANSWER:", trial["answer"])
        save_report("b5-trace.json", {"case":case, "trial":trial, "max_turns":args.max_turns})
        if trial["error"]:
            raise RuntimeError(f"Trace incomplete/failed: {trial['error']['type']}. Inspect the saved evidence.")
    else:
        cases = cases_for_run()
        probe_grader()  # A broken checker must not silently approve a comparison.
        if args.checkpoint == "baseline":
            results = direct_cases(cases, False)
            save_report("b5-baseline.json", {"cases":cases, "results":results, "execution":"offline"})
        elif args.checkpoint == "compare":
            candidate_decision(200)
            print("BASELINE")
            baseline = direct_cases(cases,False)
            print("CANDIDATE")
            candidate = direct_cases(cases,True)
            print("ADDITIONAL FEE 201:", candidate_decision(201), "EXPECTED: review")
            save_report("b5-compare.json", {"cases":cases, "baseline":baseline, "candidate":candidate, "execution":"offline"})
        else:
            candidate_decision(200)
            # Same three available/missing decision tasks as the slide comparison.
            selected = [case for case in cases if case["caller"]=="A" and not case["unavailable"]]
            if not selected:
                raise ValueError("No available/missing caller-A cases were selected.")
            print("BASELINE")
            baseline = repeat_cases(selected,False,args.repeats,args.max_turns)
            print("CANDIDATE")
            candidate = repeat_cases(selected,True,args.repeats,args.max_turns)
            save_report("b5-trials.json", {"cases":selected, "baseline":baseline, "candidate":candidate,
                                          "repeats":args.repeats, "max_turns":args.max_turns})


if __name__ == "__main__":
    run_cli(main)
