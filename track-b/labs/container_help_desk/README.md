# Container help desk · standalone lab draft

A port operations trainee needs help with shipping terminology. Later they
need recorded status and fee information for a customer enquiry, followed by
a factual update that a colleague can review.

This working draft uses a container-help-desk setting throughout B1–B5. The records are synthetic;
the USD 100 fee is a supplied classroom value, not a recreated PortOps tariff.

| Module | Instructions | Edit |
| --- | --- | --- |
| B1: explain terms and retain a conversation | [B1.md](B1.md) | [b1.py](b1.py), 3 TODO functions |
| B2: connect tools and share them through MCP | [B2.md](B2.md) | [b2.py](b2.py), 4 TODO functions |
| B3: investigate, save and review | [B3.md](B3.md) | [b3.py](b3.py), 5 core TODOs; 2 optional |
| B4: query permitted structured data | [B4.md](B4.md) | [b4.py](b4.py), 5 TODO functions |
| B5: evaluate generated answers and compare prompts | [B5.md](B5.md) | [b5.py](b5.py), 5 TODO functions |

Target 30–40 minutes for B1–B3 and 60 minutes for B4/B5, with setup completed beforehand. Keep the
implementation small, then choose two questions from that module's exploration
bank. Use the [predict/change/inspect/explain method](../EXPLORATION.md) to record
what the same lab demonstrates. Further questions and extensions are optional.

## Prepare once

From the repository root:

```bash
cd track-b/labs/container_help_desk
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

If you already prepared B1–B3, rerun the dependency-install command above for
the SQLAlchemy/LlamaIndex packages used by B4/B5. Python 3.11 or later is required. Put the approved model key in this folder's
ignored `.env`:

```dotenv
OPEN_AI_KEY=your-key-here
```

An exported key also works. Existing `.env` files in `track-b` or the repository
root are loaded without overriding exported values. Do not put keys in Python.
Hosted calls use the same GPT-4.1-mini model as the snippets.

All commands in B1.md–B5.md run **from this lab folder with this environment
active**. In a second terminal, change to this same folder and activate the
same `.venv`. File output is relative to the lab, even if a script is invoked
by absolute path from another directory.

## First run: confirm the scaffold

```bash
python b1.py
python b2.py
python b3.py
python b4.py
python b5.py
python records.py
python b1.py call
```

The first five commands show checkpoint help. `records.py` prints real reads
of the supplied fixtures; it needs no key. The last command initially prints
`TODO B1.1` and exits with status 2. That is the starting point, not a failed
model request. After implementing a function, rerun the same checkpoint.

| Identifier | Recorded status | Supplied net fee |
| --- | --- | ---: |
| C1 | OVERDUE | USD 100 |
| C2 | GATED_OUT | USD 0 |
| C3 | IN_TERMINAL | USD 0 |
| C9 | Absent | Unavailable, not zero |

B4/B5 use their own independent fixtures, matching their respective slide decks:

- **B4:** C1/A/delayed/100, C2/B/delayed/200, C4/A/delayed/50 and C5/A/on_time/75 USD. [b4_data.py](b4_data.py) builds the source and trusted A projection. Its databases reset for each command.
- **B5:** an approved text snapshot supplies C1/100 and C2/200 USD, review at 200 or more and an absent C9. No waiver/payment/release information is supplied. The task evaluates generated answers; it does not import `records.py` or B4 learner functions.

## What is already supplied

- `records.py`: small records and read functions.
- `support.py`: key setup, helpful TODO exits and local output handling.
- `mcp_server.py`: publishes your B2 read functions; port **8871**.
- The sections below the TODO functions: CLI, actual runtime calls and file handling.
- `b4_data.py`: synthetic database fixture/projection and SQLite execution policy. B4's boundaries checkpoint is already complete.

B1 connects no records. B2 does not import B1, and B3 supplies its own working
tools instead of importing unfinished B2 functions. You can start a later
module even if you did not finish the previous one. B4 and B5 likewise start independently.

B3 creates `work/conversation.db`, per-container task/pending JSON and
`work/outbox.jsonl`. Review saves a local draft only. These files are ignored
by Git. The lab models classroom review and file storage, not enterprise
identity, transactional recovery or customer messaging.

B5 writes `work/b5-generated-answer.json`, `b5-evaluate.json`,
`b5-calibration.json`, `b5-dataset.json` and `b5-compare-prompts.json`.
Each checkpoint replaces its own report, retaining actual text, references,
judge feedback/status and configuration. Generation/judge failures remain
visible. Only B5's `cases` checkpoint is offline. B4 needs no persistent file
or server. The prior [rule-testing lab](B5-APPLICATION-CHECKS-REFERENCE.md)
remains a supporting reference.

Only this standalone version is currently distributed. The timing target still
needs an instructor dry run; see the [course map](../../README.md).

