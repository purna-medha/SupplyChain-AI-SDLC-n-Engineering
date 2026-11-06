"""Application adapter for 02_evaluate_cases.yaml. No model or grader here."""

import json


def call_api(prompt, options, context):
    case = context["vars"]
    record = {"C1": ("A", 100), "C2": ("A", 200)}.get(case["container_id"])
    if record is None:
        actual = [None, "unknown"]
    elif case["caller"] != record[0]:
        actual = [None, "denied"]
    elif case["unavailable"]:
        actual = [None, "unavailable"]
    else:
        fee = record[1]
        actual = [fee, "review" if fee > 200 else "clear"]  # Deliberate defect.
    return {"output": json.dumps(actual)}
