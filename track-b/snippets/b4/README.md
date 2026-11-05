# B4 · Enterprise data and governed reads

Only the essential worked examples are in this folder. Run them in order; the same complete file is both the snippet and the instructor-led code-along. Each file adds a mechanism needed to understand this module.

| File | Why it is essential | One learner change |
| --- | --- | --- |
| [01_query_and_check_grain.py](01_query_and_check_grain.py) | Expose a wrong join result and its grain-preserving repair. | give C1 and C2 equal fees; explain why SUM(DISTINCT fee) is not a repair. |
| [02_generate_and_validate_sql.py](02_generate_and_validate_sql.py) | Generate against a schema and compare with an independent reference. | ask for the maximum fee and independently state the expected result first. |
| [03_governed_read_capability.py](03_governed_read_capability.py) | Make caller scope, field selection and a result bound executable. | request C2 as owner A, then request more than the allowed row count. |

From `track-b`: `python codealongs/b4/01_query_and_check_grain.py`. Read [setup](../../SETUP.md) once. Each example is independent, with tiny synthetic data and direct calls to the library or Python operation being taught. Repeated setup keeps the full operation visible. There are no learner gaps or project imports.

SQLite supplies the disposable local SQL lesson; the same contract maps to an approved DuckDB, warehouse or service boundary. These examples do not provide a production text-to-SQL sandbox. Enterprise identity, replicas and resource controls remain design discussion.

The default model examples call OpenAI through the documented libraries. They load `OPENAI_API_KEY` with dotenv. No canned output or fake successful model run replaces missing access. Labs are deferred. Earlier versions are preserved under `authoring/previous-codealongs-before-essential-selection`, outside the teaching path.
