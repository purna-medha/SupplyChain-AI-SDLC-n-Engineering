"""B5 learner starter: evaluate actual generated answers and compare prompts.

Five TODO functions. No reference answer is passed to the generation function.
Supplied runners retain raw answers, judge feedback, errors and fixed denominators.
"""

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
from time import perf_counter

from llama_index.core import Settings
from llama_index.core.evaluation import AnswerRelevancyEvaluator, CorrectnessEvaluator, FaithfulnessEvaluator
from llama_index.llms.openai import OpenAI

from support import WORK, run_cli

MODEL = "gpt-4.1-mini"
BASELINE = "Answer the shipping enquiry helpfully."
CONTEXT = """Synthetic snapshot fees-v1, observed 2026-11-06T00:00:00Z.
C1: recorded fee USD 100; status on_time. C2: recorded fee USD 200; status delayed.
Recorded fees of USD 200 or more require review. C9 has no matching record.
No waiver, payment or release schedule information is supplied."""
THRESHOLDS = {"correctness":4.0, "grounding":1.0, "relevance":1.0}
RANGES = {"correctness":(1.0,5.0), "grounding":(0.0,1.0), "relevance":(0.0,1.0)}
HELD_OUT = {
    "id":"comparison", "split":"held_out", "context":CONTEXT,
    "question":"Compare C1 and C2's recorded fees and review requirements.",
    "reference":"C1 has a recorded fee of USD 100, below the review threshold. C2 has USD 200 and requires review.",
}


def make_cases() -> list[dict]:
    """B5.1: four development cases, with independent reference answers."""
    # TODO: dictionaries with id, question, context and reference.
    # Cover a known fee, missing C9, tomorrow's release, and an unsupported waiver premise.
    # Use CONTEXT. Derive references from those facts/policy, not from generated answers.
    raise NotImplementedError("TODO B5.1: implement make_cases")


def generate_answer(generator, instruction: str, question: str, context: str) -> str:
    """B5.2: generate a real answer using ONLY instruction, question and context."""
    # TODO: generator.complete(your prompt).text. No reference argument is supplied here.
    raise NotImplementedError("TODO B5.2: implement generate_answer")


def make_evaluators(judge) -> dict:
    """B5.3: configure separate correctness, grounding and relevance evaluators."""
    # TODO: return {"correctness":CorrectnessEvaluator(llm=judge),
    # "grounding":FaithfulnessEvaluator(llm=judge),
    # "relevance":AnswerRelevancyEvaluator(llm=judge)}.
    raise NotImplementedError("TODO B5.3: implement make_evaluators")


def evaluate_answer(evaluator, case: dict, answer: str):
    """B5.4: give the evaluator the actual answer and appropriate evidence/reference."""
    # TODO: evaluator.evaluate(query=case["question"], response=answer,
    #                         reference=case["reference"], contexts=[case["context"]]).
    # Each evaluator uses its relevant inputs; references never go to generation.
    raise NotImplementedError("TODO B5.4: implement evaluate_answer")


def candidate_instruction() -> str:
    """B5.5: write one prompt change addressing failures in DEVELOPMENT answers."""
    # TODO: explicit evidence use, uncertainty and unsupported-premise handling.
    # Keep questions, contexts, references, judges and thresholds fixed for comparison.
    raise NotImplementedError("TODO B5.5: implement candidate_instruction")


# Supplied execution/reporting below. Learners work in the five functions above.
def metric_record(name, result):
    score = result.score
    low, high = RANGES[name]
    valid = (not result.invalid_result and type(score) in (int,float)
             and math.isfinite(score) and low <= score <= high)
    return {"status":"valid" if valid else "invalid", "score":score if valid else None,
            "passed":valid and score >= THRESHOLDS[name], "feedback":result.feedback,
            "invalid_reason":getattr(result,"invalid_reason",None), "raw_score":str(score)}


def run_case(generator, evaluators, case, instruction):
    started = perf_counter()
    trial = {"case_id":case["id"], "question":case["question"], "context":case["context"],
             "reference":case["reference"], "answer":None, "generation_error":None,
             "metrics":{}, "passed":False}
    try:
        trial["answer"] = generate_answer(generator,instruction,case["question"],case["context"])
        if not isinstance(trial["answer"],str) or not trial["answer"].strip():
            raise RuntimeError("Generation returned no usable answer.")
        print("GENERATED ANSWER:",trial["answer"])
    except NotImplementedError:
        raise
    except Exception as error:
        trial["generation_error"] = {"type":type(error).__name__, "message":str(error)}
    if trial["generation_error"] is None:
        for name in THRESHOLDS:
            try:
                result = evaluate_answer(evaluators[name],case,trial["answer"])
                trial["metrics"][name] = metric_record(name,result)
            except NotImplementedError:
                raise
            except Exception as error:
                trial["metrics"][name] = {"status":"error", "score":None, "passed":False,
                                          "error":{"type":type(error).__name__,"message":str(error)}}
            print("METRIC:",name,trial["metrics"][name])
        trial["passed"] = all(item["passed"] for item in trial["metrics"].values())
    else:
        print("GENERATION ERROR:",trial["generation_error"])
    trial["seconds"] = round(perf_counter()-started,3)  # Generation plus judge work.
    return trial


def compare_prompts(generator, evaluators, cases, candidate, repeats):
    if repeats < 1 or not cases or not isinstance(candidate,str) or not candidate.strip():
        raise ValueError("Provide cases, a nonempty candidate and positive repeats.")
    trials = []
    for version,instruction in [("baseline",BASELINE),("candidate",candidate)]:
        for case in cases:
            for attempt in range(repeats):
                print("VERSION:",version,"CASE:",case["id"],"ATTEMPT:",attempt+1)
                trial = run_case(generator,evaluators,case,instruction)
                trial.update(version=version,split=case["split"],attempt=attempt+1)
                trials.append(trial)  # No failure/invalid judgment is removed.
    for version in ["baseline","candidate"]:
        for split in ["development","held_out"]:
            selected = [t for t in trials if t["version"]==version and t["split"]==split]
            if selected:
                print("SUMMARY:",version,split,sum(t["passed"] for t in selected),"/",len(selected))
    return trials


def cases_for_run():
    cases = make_cases()
    if not cases or len({case["id"] for case in cases}) != len(cases):
        raise ValueError("Provide a nonempty development set with unique IDs.")
    for case in cases:
        if not all(isinstance(case.get(key),str) and case[key].strip()
                   for key in ["id","question","context","reference"]):
            raise ValueError("Each case needs nonempty id/question/context/reference strings.")
        if case["id"] == HELD_OUT["id"]:
            raise ValueError("Keep the supplied held-out case separate from development.")
    return [dict(case,split="development") for case in cases]


def clients():
    key = os.environ.get("OPEN_AI_KEY")
    if not key:
        raise ValueError("Set OPEN_AI_KEY in the lab .env or export it before model calls.")
    Settings.embed_model = None
    return (OpenAI(model=MODEL,temperature=0,max_tokens=200,api_key=key),
            OpenAI(model=MODEL,temperature=0,max_tokens=512,api_key=key))


def save_report(filename, report):
    WORK.mkdir(parents=True,exist_ok=True)
    report.update(generator_model=MODEL,judge_model=MODEL,thresholds=THRESHOLDS,
                  code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  missing_token_usage="unknown",elapsed_scope="generation and evaluation")
    path = WORK/filename
    path.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print("EVIDENCE:",path)


def calibrate(evaluators):
    case = {"id":"calibration", "context":CONTEXT,
            "question":"Explain C2's recorded fee, review requirement and release date.",
            "reference":"C2 has a recorded fee of USD 200 and requires review. The supplied information does not establish a release date."}
    probes = [
        ("correct",case["reference"],True),
        ("wrong amount","C2's recorded fee is USD 999 and review is needed. Its release date is unknown.",False),
        ("unsupported release","C2's recorded fee is USD 200 and review is needed. It will be released tomorrow.",False),
        ("unsupported denial","C2's recorded fee is USD 200 and review is needed. It will not be released tomorrow.",False),
        ("paraphrase","The record lists 200 US dollars for C2, so review is needed. The facts do not establish a release date.",True),
    ]
    results = []
    for label,answer,expected in probes:
        # The author label stays outside the case passed to the evaluator.
        for name in ["correctness","grounding"]:
            try:
                recorded = metric_record(name,evaluate_answer(evaluators[name],case,answer))
                match = recorded["status"]=="valid" and recorded["passed"]==expected
            except NotImplementedError:
                raise
            except Exception as error:
                recorded,match = {"status":"error","error":str(error)},False
            row = {"probe":label,"prepared_answer":answer,"expected_acceptance":expected,
                   "metric":name,"judgment":recorded,"agreement":match}
            results.append(row)
            print("CALIBRATION:",row)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint",nargs="?",choices=["cases","generate","evaluate","calibrate","dataset","compare"])
    parser.add_argument("--case",help="Restrict generation/evaluation to this case ID")
    parser.add_argument("--repeats",type=int,default=1)
    args = parser.parse_args()
    if args.checkpoint is None:
        parser.print_help()
        return
    if args.repeats < 1:
        raise ValueError("Repeats must be positive.")
    if args.checkpoint == "calibrate":
        _,judge = clients()
        save_report("b5-calibration.json",{"probes":calibrate(make_evaluators(judge))})
        return
    cases = cases_for_run()
    if args.checkpoint == "cases":
        print(json.dumps(cases,indent=2))
        return
    if args.checkpoint == "compare":
        candidate = candidate_instruction()  # Fail visibly before paid work if unfinished.
        cases.append(dict(HELD_OUT))
    if args.case:
        cases = [case for case in cases if case["id"]==args.case]
        if not cases:
            raise ValueError("No matching case ID.")
    generator,judge = clients()
    if args.checkpoint == "generate":
        case = cases[0]
        answer = generate_answer(generator,BASELINE,case["question"],case["context"])
        print("GENERATED ANSWER:",answer)
        save_report("b5-generated-answer.json",{"case":case,"answer":answer,"instruction":BASELINE})
        return
    evaluators = make_evaluators(judge)
    if args.checkpoint == "compare":
        trials = compare_prompts(generator,evaluators,cases,candidate,args.repeats)
        save_report("b5-compare-prompts.json",{"cases":cases,"prompts":{"baseline":BASELINE,"candidate":candidate},
                                            "repeats":args.repeats,"trials":trials})
    else:
        selected = cases[:1] if args.checkpoint=="evaluate" else cases
        trials = [run_case(generator,evaluators,case,BASELINE) for case in selected]
        save_report("b5-"+args.checkpoint+".json",{"cases":selected,"instruction":BASELINE,"trials":trials})


if __name__ == "__main__":
    run_cli(main)
