"""Check a prepared answer against a trusted record. No model call.

Try: change the draft fee from 999 to 200, then change only its text.
"""

facts = {"container_id": "C2", "fee": 200, "source": "fees-v1"}
draft = {"container_id": "C2", "fee": 999, "source": "fees-v1",
         "text": "Your recorded fee is ready."}

checks = {
    "required fields": all(field in draft for field in facts),
    "fee type": type(draft.get("fee")) is int,
    "correct container": draft.get("container_id") == facts["container_id"],
    "correct amount": draft.get("fee") == facts["fee"],
    "source label": draft.get("source") == facts["source"],
}
for requirement, passed in checks.items():
    print(requirement, "PASS" if passed else "FAIL")

# These field checks do not evaluate the meaning or clarity of draft["text"].
