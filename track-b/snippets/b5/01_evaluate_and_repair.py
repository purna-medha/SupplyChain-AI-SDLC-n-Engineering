"""Define expected cases, expose a boundary failure, then compare one repair.

Try: change the threshold and update independent expectations before running.
"""

records = {"C1": ("A", 100), "C2": ("A", 200), "C3": ("A", 201)}
# Classroom policy: owner access and fee >= 200 requires review.
cases = [
    ("normal", "A", "C3", "review"),
    ("equality", "A", "C2", "review"),
    ("below", "A", "C1", "clear"),
    ("missing", "A", "C9", "unknown"),
    ("denied", "B", "C2", "denied"),
]
for version in ["before", "after"]:
    passed = 0
    for name, caller, container_id, expected in cases:
        record = records.get(container_id)
        if record is None:
            actual = "unknown"
        elif caller != record[0]:
            actual = "denied"
        else:
            fee = record[1]
            review = fee > 200 if version == "before" else fee >= 200
            actual = "review" if review else "clear"
        correct = actual == expected
        passed += correct
        print(
            version,
            name,
            "expected:",
            expected,
            "actual:",
            actual,
            "PASS" if correct else "FAIL",
        )
    print(version, "score:", passed, "/", len(cases))
