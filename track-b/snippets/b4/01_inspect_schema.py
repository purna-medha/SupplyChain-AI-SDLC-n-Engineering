"""Inspect real tables, keys and relationships with SQLAlchemy. No model call.

Try: identify what one row represents before looking at the inspector output.
"""

from sqlalchemy import create_engine, inspect

engine = create_engine("sqlite://")
with engine.begin() as connection:
    connection.exec_driver_sql("CREATE TABLE containers (id TEXT PRIMARY KEY, owner TEXT, status TEXT)")
    connection.exec_driver_sql("CREATE TABLE fees (container_id TEXT PRIMARY KEY REFERENCES containers(id), fee INTEGER, currency TEXT)")
    connection.exec_driver_sql("INSERT INTO containers VALUES ('C1','A','delayed'), ('C2','B','delayed')")
    connection.exec_driver_sql("INSERT INTO fees VALUES ('C1',100,'USD'), ('C2',200,'USD')")

inspector = inspect(engine)
for table in inspector.get_table_names():
    print("\nTABLE:", table)
    print("COLUMNS:", [(col["name"], str(col["type"])) for col in inspector.get_columns(table)])
    print("PRIMARY KEY:", inspector.get_pk_constraint(table)["constrained_columns"])
    print("FOREIGN KEYS:", inspector.get_foreign_keys(table))
engine.dispose()
# Keys describe structure. Business definitions such as "outstanding fee" need human context.
