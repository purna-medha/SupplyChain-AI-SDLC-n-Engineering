"""B1 lab: parse a candidate note, validate its shape, then check scope.
Run this file directly after filling the gap. No capstone imports are needed.
"""
from typing import Literal
from pydantic import BaseModel, ConfigDict

class ContainerNote(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    container_id: str
    status: Literal["delayed", "on_time"]

def parse_and_check(raw, allowed_ids):
    # TODO: validate raw with ContainerNote.model_validate_json.
    # TODO: reject a container outside allowed_ids with PermissionError.
    # TODO: return the validated note as a dictionary.
    raise NotImplementedError("Use the schema, then the business rule")

allowed = {"C1"}
good = '{"container_id":"C1","status":"delayed"}'
assert parse_and_check(good, allowed)["status"] == "delayed"
for candidate in [
    '{"container_id":"C1","status":"maybe"}',
    '{"container_id":"C2","status":"delayed"}',
]:
    try:
        parse_and_check(candidate, allowed)
    except (ValueError, PermissionError) as error:
        print("Expected rejection:", type(error).__name__)
    else:
        raise AssertionError("This candidate should have been rejected")
print("The schema and permission checks behaved as expected.")
