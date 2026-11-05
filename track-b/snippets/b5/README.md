# B5 · Evaluation, tracing and improvement

Only the essential worked examples are in this folder. Run them in order; the same complete file is both the snippet and the instructor-led code-along. Each file adds a mechanism needed to understand this module.

| File | Why it is essential | One learner change |
| --- | --- | --- |
| [01_evaluate_and_repair.py](01_evaluate_and_repair.py) | Turn requirements into cases and demonstrate a measured repair. | change the threshold and update independent expectations before running. |
| [02_trace_actual_work.py](02_trace_actual_work.py) | Capture actual read/model evidence, duration and usage. | change the requested ID; inspect the observation before judging the reply. |
| [03_rubric_judge.py](03_rubric_judge.py) | Separate known facts from rubric-based quality judgment. | set the prepared fee to 999; the factual check stops before the model call. |

From `track-b`: `python codealongs/b5/01_evaluate_and_repair.py`. Read [setup](../../SETUP.md) once. Each example is independent, with tiny synthetic data and direct calls to the library or Python operation being taught. Repeated setup keeps the full operation visible. There are no learner gaps or project imports.

The trace is local JSON evidence, suitable for understanding before an approved Langfuse integration. Metric definitions, costs and evaluation-framework comparisons stay in the slides. The judge rates clarity after known facts pass; it grants no action authority.

The default model examples call OpenAI through the documented libraries. They load `OPENAI_API_KEY` with dotenv. No canned output or fake successful model run replaces missing access. Labs are deferred. Earlier versions are preserved under `authoring/previous-codealongs-before-essential-selection`, outside the teaching path.
