"""Supply a schema, inspect actual generated SQL, and compare its result.

Try: ask for the maximum fee and independently state the expected result first.
This disposable SQLite example is not a production SQL security boundary.
"""

import os
import sqlite3
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
connection = sqlite3.connect(":memory:")
connection.executescript("""
CREATE TABLE containers (id TEXT PRIMARY KEY, fee INTEGER);
INSERT INTO containers VALUES ('C1', 100), ('C2', 200);
""")
connection.execute("PRAGMA query_only = ON")
connection.set_progress_handler(lambda: 1, 10000)
response = completion(
    model="openai/gpt-4.1-mini",
    api_key=os.environ["OPEN_AI_KEY"],
    messages=[
        {
            "role": "system",
            "content": "Return one plain SQLite SELECT without fences. "
            "Schema: containers(id TEXT PRIMARY KEY, fee INTEGER). One row per container.",
        },
        {"role": "user", "content": "What is the total fee?"},
    ],
)
sql = response.choices[0].message.content
print("Actual SQL:", sql)
try:
    rows = connection.execute(sql).fetchmany(3)
    print("Actual result:", rows)
    print("Independently expected:", [(300,)])
    print("Correct:", rows == [(300,)])
except (sqlite3.Error, TypeError) as error:
    print("Rejected or failed:", error)
connection.close()
