"""Use a fixed query, trusted caller and typed business result. No model call.

Try: request C2 or C9, then bind C1' OR 1=1 -- as the complete ID value.
"""

from datetime import datetime
from pydantic import BaseModel, StrictInt
from sqlalchemy import create_engine, text


class FeeRecord(BaseModel):
    container_id: str
    fee: StrictInt
    currency: str
    as_of: datetime
    source: str = "training-db"


engine = create_engine("sqlite://")
with engine.begin() as connection:
    connection.exec_driver_sql("""
        CREATE TABLE container_fees (container_id TEXT PRIMARY KEY, owner TEXT,
            fee INTEGER, currency TEXT, as_of TEXT, private_note TEXT)
    """)
    connection.exec_driver_sql("""
        INSERT INTO container_fees VALUES
        ('C1','A',100,'USD','2026-11-06T00:00:00Z','internal-only'),
        ('C2','B',200,'USD','2026-11-06T00:00:00Z','internal-only')
    """)
trusted_owner = "A"  # Host identity fixture, not supplied by the model.
container_id = "C1"
with engine.connect() as connection:
    row = connection.execute(text(
        "SELECT container_id, fee, currency, as_of FROM container_fees "
        "WHERE container_id = :id AND owner = :owner LIMIT 1"
    ), {"id": container_id, "owner": trusted_owner}).mappings().first()
if row is None:
    print("RESULT: unavailable")
else:
    print("RESULT:", FeeRecord.model_validate(dict(row)).model_dump(mode="json"))
engine.dispose()
# Binding fixes SQL structure. The separate owner predicate supplies this tool's row scope.
# A typed result checks its shape; it does not prove business meaning or authorisation.
