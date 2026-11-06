"""Run independent cases against a fee decision. No model call.

Classroom policy: the owner may read the fee; 200 USD or more needs review.
Try: predict the boundary case before running.
"""


def get_fee_decision(caller, container_id, unavailable=False):
    records = {"C1": ("A", 100), "C2": ("A", 200)}
    record = records.get(container_id)
    if record is None:
        return None, "unknown"
    owner, fee = record
    if caller != owner:
        return None, "denied"
    if unavailable:
        return None, "unavailable"
    return fee, "review" if fee > 200 else "clear"  # Deliberate boundary defect.


# References come from the policy, independently of the function above.
cases = [
    ("below", "A", "C1", False, (100, "clear")),
    ("boundary", "A", "C2", False, (200, "review")),
    ("missing", "A", "C9", False, (None, "unknown")),
    ("denied", "B", "C2", False, (None, "denied")),
    ("dependency", "A", "C2", True, (None, "unavailable")),
]
passed = 0
for name, caller, container_id, unavailable, expected in cases:
    actual = get_fee_decision(caller, container_id, unavailable)
    correct = actual == expected
    passed += correct
    print(name, "expected:", expected, "actual:", actual, "PASS" if correct else "FAIL")
print("Passed:", passed, "/", len(cases))
# unavailable=True is a controlled source outcome, not a real service outage.
