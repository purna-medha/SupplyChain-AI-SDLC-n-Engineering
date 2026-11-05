# B1–B3 code exploration notebooks

The snippets show the smallest useful mechanism. These notebooks let learners
open it up, inspect intermediate objects and vary one assumption at a time.
Each experiment follows **predict → run → inspect → change one thing**.

| Module | Notebook | Deeper questions |
| --- | --- | --- |
| B1 | [Messages, tokens and generation](b1_messages_tokens_and_generation.ipynb) | Are words tokens? Can a token split a character? What does request usage count? Where does follow-up context come from? Why can a nonempty answer be incomplete? |
| B2 | [Tools, contracts and MCP](b2_tools_contracts_and_mcp.ipynb) | What does a schema disclose? When does a function execute? How do invalid arguments, unknown records and denied reads differ? Is MCP discovery execution? |
| B3 | [Workflows, state and approval](b3_workflows_state_and_approval.ipynb) | Who selects the next step? Can work happen before a turn limit? Who owns the final reply? Why is a session ID insufficient without its store? What state actually resumes a paused action? |

All experiment code is complete. Participants can run and modify it before
attempting the [application TODO labs](../labs/README.md). No lab answers are
filled in. The notebooks use the existing synthetic shipping examples; they
do not require the PortOps backend.

B1 expands the model-call, instruction, history, tokenizer and measurement
snippets. B2 expands the ordinary function, SDK agent and shared MCP pair.
B3 expands workflow, investigation, delegation, memory and approval snippets;
file-backed session/runtime state are treated as deeper follow-ons.

## Prepare the notebook environment

From the repository root:

```bash
cd track-b
python3 -m venv notebooks/.venv
source notebooks/.venv/bin/activate
python -m pip install -r notebooks/requirements.txt
python -m ipykernel install --user --name maersk-exploration --display-name "Maersk exploration"
python -m jupyterlab notebooks
```

Use Python 3.11 or later. Select **Maersk exploration** as the notebook kernel.
In VS Code, opening an `.ipynb` and selecting `notebooks/.venv/bin/python`
is an alternative. A kernel is the Python process holding notebook variables;
installing a package into another environment does not update that process.

Put `OPEN_AI_KEY` in the ignored `notebooks/.env`, or export it. Setup also
loads the existing `snippets/.env`, `track-b/.env` and repository-root `.env`
without overriding exported values. No key is printed or stored in outputs.

## Choose what to execute

- **Default:** Run All executes tokenization, prepared tool-boundary probes,
  routing and storage experiments. Live calls are explicitly marked SKIPPED.
  No model response is fabricated. The tokenizer may download its vocabulary
  once; prepare its cache before a fully offline class.
- **Model experiments:** set the visible `RUN_LIVE = True` in setup, then
  restart the kernel and Run All. Requests use the same GPT-4.1-mini as the
  snippets and incur actual API usage. Missing credentials and service errors
  surface as errors.
- **B1 local model:** enable `RUN_LOCAL` only after the snippet's Ollama
  preparation. It is independent of hosted-model access.
- **B2 MCP:** run `python snippets/b2/04_shared_mcp_server.py` from `track-b`
  in another prepared terminal, then enable `RUN_MCP`. Discovery and direct
  invocation need no model key. The remote-agent comparison needs both switches.
- **B3 specialists:** enable `RUN_DELEGATION` with live inference to compare
  coordinator ownership with a handoff. Nested model calls have their own costs.
- **B3 review:** inspect the printed pending payload, then choose the decision
  in the next cell. The default is rejection. The only action affects an
  in-memory demonstration outbox; it sends no message.

## A useful way to work

Read the question and write a prediction before running the cell. Inspect
returned fields, read logs and stored state before interpreting final prose.
Change one input, rerun the cell that defines it and its dependent cells, and
explain the resulting difference.

Restart and Run All to establish a clean baseline. For B3's approval comparison,
rerun the proposal and snapshot cells before applying another decision.
Running the same resumed state again is not a fresh approval experiment.

Default execution is not evidence that the model, local inference or MCP
worked. Use actual live outputs for those claims. Distributed notebooks have
empty output cells so previous observations cannot be mistaken for a new run.
The approval cells publish only a validated proposal, clear stale pending
state and consume each restored state once. A failed cell is not permission
to continue with an older proposal; create a fresh one.

## Relationship to the course

Use the [slides](../slides-md/README.md) to establish the concepts, the
[short snippets](../snippets/README.md) to inspect the essential code, these
notebooks to explore mechanisms, and the [TODO labs](../labs/README.md) to
apply them to a use case. Learners can select relevant experiments; these
notebooks do not add required lecture time to the workshop allocation.

See the [verification record](VERIFICATION.md) for executed paths and limits.
