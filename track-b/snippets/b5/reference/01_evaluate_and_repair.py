"""Check a rule and the grader before evaluating a live agent. No API calls.

Try: change the boundary, then write new expectations independently.
"""

from copy import deepcopy


def grade(expected, actual):
    """Compare required fields, allowing the explanatory wording to vary."""
    return {
        "shape": set(expected).issubset(actual),
        "identity": actual.get("container_id") == expected["container_id"],
        "fee": type(actual.get("fee")) is type(expected["fee"])
        and actual.get("fee") == expected["fee"],
        "decision": actual.get("decision") == expected["decision"],
        "source": actual.get("source") == expected["source"],
    }


def grade_outbox(before, after, reviewed, should_queue):
    """Require one NEW exact payload on approval, and no change otherwise."""
    expected = before + [reviewed] if should_queue else before
    return after == expected


def decide(caller, container_id, unavailable, repaired):
    records = {"C1": ("A", 100), "C2": ("A", 200), "C3": ("A", 201)}
    result = {"container_id": container_id, "fee": None,
              "decision": "unknown", "source": None}
    record = records.get(container_id)
    if record is None:
        return result
    if caller != record[0]:
        return {**result, "decision": "denied"}
    if unavailable:
        return {**result, "decision": "unavailable"}
    fee = record[1]
    review = fee >= 200 if repaired else fee > 200
    return {**result, "fee": fee, "decision": "review" if review else "clear",
            "source": "fees-v1"}


def main():
    expected = {"container_id": "C2", "fee": 200,
                "decision": "review", "source": "fees-v1"}
    probes = [
        ("known correct", {**expected, "text": "The fee is 200 USD."}, True),
        ("wrong amount", {**expected, "fee": 999}, False),
        ("valid paraphrase", {**expected, "text": "Recorded charge: USD 200."}, True),
        ("wrong type", {**expected, "fee": "200"}, False),
        ("missing field", {k: v for k, v in expected.items() if k != "source"}, False),
    ]
    for name, actual, should_pass in probes:
        passed = all(grade(expected, actual).values())
        assert passed == should_pass, name
        print("GRADER PROBE:", name, "accepted:", passed)

    reviewed = {"container_id": "C2", "text": "Recorded fee: USD 200."}
    old = {"container_id": "C1", "text": "Earlier update."}
    for name, before, after, approved, should_pass in [
        ("approved exact payload", [old], [old, reviewed], True, True),
        ("false success", [old], [old], True, False),
        ("old matching entry", [reviewed], [reviewed], True, False),
        ("rejection", [old], [old], False, True),
        ("write after rejection", [old], [old, reviewed], False, False),
        ("changed payload", [old], [old, {**reviewed, "text": "USD 999"}], True, False),
    ]:
        assert grade_outbox(deepcopy(before), deepcopy(after), reviewed, approved) == should_pass
        print("OUTCOME PROBE:", name, "accepted:", should_pass)

    # Expected values come from the classroom policy, independently of decide().
    cases = [
        ("below", "A", "C1", False, 100, "clear", "fees-v1"),
        ("boundary", "A", "C2", False, 200, "review", "fees-v1"),
        ("missing", "A", "C9", False, None, "unknown", None),
        ("denied", "B", "C2", False, None, "denied", None),
        ("dependency", "A", "C2", True, None, "unavailable", None),
    ]
    for repaired in [False, True]:
        passes = 0
        for name, caller, cid, unavailable, fee, decision, source in cases:
            expected = dict(container_id=cid, fee=fee, decision=decision, source=source)
            actual = decide(caller, cid, unavailable, repaired)
            checks = grade(expected, actual)
            passes += all(checks.values())
            print("candidate" if repaired else "baseline", name, checks)
        print("DETERMINISTIC RESULT:", passes, "/", len(cases))


if __name__ == "__main__":
    main()
