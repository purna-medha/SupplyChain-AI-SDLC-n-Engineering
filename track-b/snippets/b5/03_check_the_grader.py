"""Check the checker using known results. No model call.

Try: make the grader always return True. Which probe exposes the defect?
"""


def correct_fee(answer):
    return (answer.get("container_id") == "C2"
            and type(answer.get("fee")) is int and answer["fee"] == 200)


probes = [
    ("known correct", {"container_id": "C2", "fee": 200}, True),
    ("wrong amount", {"container_id": "C2", "fee": 999}, False),
    ("wrong container", {"container_id": "C1", "fee": 200}, False),
    ("wrong type", {"container_id": "C2", "fee": "200"}, False),
    ("missing fee", {"container_id": "C2"}, False),
]
for name, answer, expected in probes:
    actual = correct_fee(answer)
    print(name, "expected acceptance:", expected, "actual:", actual)
    assert actual == expected, f"Grader defect: {name}"

# Wording is outside this check. Example 07 separately checks clarity/paraphrases.
