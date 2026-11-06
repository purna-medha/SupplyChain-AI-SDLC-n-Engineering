"""A grader probe passes when acceptance agrees with the known probe label."""

import json


def correct_fee(answer):
    return (answer.get("container_id") == "C2"
            and type(answer.get("fee")) is int and answer["fee"] == 200)


def get_assert(output, context):
    accepted = correct_fee(json.loads(output))
    expected = context["vars"]["expected_acceptance"]
    passed = accepted == expected
    return {"pass": passed, "score": int(passed),
            "reason": f"Expected acceptance: {expected}; actual acceptance: {accepted}"}
