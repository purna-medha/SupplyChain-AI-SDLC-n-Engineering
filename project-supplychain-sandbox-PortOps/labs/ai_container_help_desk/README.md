# Container help desk · PortOps capstone lab

Apply B1–B3 to the existing SupplyChainOps application: explain port terminology,
answer a container's status/fee enquiry, then prepare an update for human review.
This is the capstone version of the [standalone lab](../../../track-b/labs/container_help_desk/README.md).
Use either version for the core workshop; the TODOs and checkpoints match.

| Module | Instructions | Capstone contribution |
| --- | --- | --- |
| B1 | [B1.md](B1.md), edit [b1.py](b1.py) | A terminology-help component; no operational data yet |
| B2 | [B2.md](B2.md), edit [b2.py](b2.py) | Model-facing tools over existing container and fee APIs |
| B3 | [B3.md](B3.md), edit [b3.py](b3.py) | Read-based investigation, saved draft, conversation and reviewed local outbox |

## 1. Start the existing capstone backend

In terminal A, from the repository root:

```bash
cd project-supplychain-sandbox-PortOps
uv sync --group dev
uv run uvicorn supplychainops.main:app --port 8002
```

Use the seeded database already prepared for the capstone. For a fresh training
copy with no seed data, initialize it with `uv run python scripts/reset_database.py`
before starting the server. That command resets exercise data; it is not part
of the repeated AI lab workflow.

The [codebase guide](../../CODEBASE_GUIDE.md) explains the API and business
rules. Leave the backend running. The dashboard can run alongside the lab;
these CLI tools use the same HTTP boundary. No dashboard changes are required.

## 2. Prepare the separate learner environment

In terminal B, from the repository root:

```bash
cd project-supplychain-sandbox-PortOps/labs/ai_container_help_desk
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Python 3.11 or later is required. This separate environment adds the AI
libraries without changing the capstone package's dependencies. Put these
settings in this folder's ignored `.env`, or export them:

```dotenv
OPEN_AI_KEY=your-key-here
PORTOPS_URL=http://127.0.0.1:8002
PORTOPS_IMPORTER=IMP-GULF-001
```

Existing `.env` files in the PortOps or repository root are also loaded;
exported values take precedence. Hosted calls use the snippets' GPT-4.1-mini.

**All commands in B1.md–B3.md run from this lab folder with its environment
active.** B2's MCP server needs a third terminal in the same folder/environment.
Its default port is **8872**, distinct from the standalone lab's 8871.

## 3. Confirm the supplied API adapter

```bash
python b1.py
python b2.py
python b3.py
python records.py
python b1.py call
```

The first three show help. `records.py` prints the health check, scoped
container overviews and actual calculated fees; no model key is used for those
reads. The last command initially reports `TODO B1.1` and exits with status 2.
Only TODO bodies in the three starter files are learner implementation work.

| Seed case with default importer | Expected observation |
| --- | --- |
| MSKU1234567, the default | Still at the terminal; overdue on the workshop date; fee from the API |
| MSCU7654321 | GATED_OUT; zero fee in the supplied seed story |
| TCLU9876543 | Belongs to IMP-GULF-002; unavailable under the default scope |
| C9 | Absent; no invented status or zero fee |

Try an ID from the table with `--container`. Fees for open containers depend
on the server's calculation date and existing approved waivers. Compare the
returned breakdown instead of memorizing a fee. To use another importer,
change `PORTOPS_IMPORTER` and restart the client/MCP server.

## How this fits into the capstone

```text
CLI help desk -> agent tool -> supplied records.py -> PortOps GET API
                                                   -> existing services
                                                   -> existing pure fee engine
```

`records.py` gets `/containers?importer_identifier=...`, then checks the ID's
membership before calling `/containers/{id}/demurrage-calculation`. Learners
implement the model-facing contracts, not tariff math or SQL. The API's exact
labels are OVERDUE, IN_TERMINAL and GATED_OUT; a C1/delayed fixture is not a
PortOps record. Existing HTTP endpoints do not supply tracking events or a
scheduled departure, so this lab does not claim to investigate those facts.

The importer setting is a classroom data scope, not authentication. Later
modules can add authenticated identity and governed access. The lab does not
expose claim submission, waiver override or gate-out operations to the agent.

B1 reads no records. B2 starts independently of B1. B3 supplies complete read
tools so it can run without completing B2. Both its investigator and the MCP
server obtain facts through this adapter; no backend implementation changes
are necessary.

B3 writes conversation/task/pending files and `work/outbox.jsonl` locally in
this lab. The reviewed action saves the exact draft there; it sends no
customer message and performs no financial/operational write. This is a
capstone extension at the application boundary, with UI integration and
production recovery left for later work.
