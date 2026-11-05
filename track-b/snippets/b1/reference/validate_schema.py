"""Use Pydantic to distinguish parseable JSON from an accepted note.

Try: change delayed to maybe, omit status, or add an extra field.
"""

from typing import Literal
from pydantic import BaseModel, ConfigDict, ValidationError


class ContainerNote(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    container_id: str
    status: Literal["delayed", "on_time"]


# Prepared JSON isolates validation from model variability.
raw = '{"container_id": "C1", "status": "delayed"}'
try:
    note = ContainerNote.model_validate_json(raw)
    print("Accepted:", note.model_dump())
except ValidationError as error:
    print("Rejected:", error.errors())
