# Track B · Essential snippets and code-alongs

**30 core B1–B6 files, plus 14 B0 preparatory snippets.** A complete file serves as both the worked illustration and the code-along. Explain the concept first, run selected examples, then change one input and inspect the actual result.

Start with [B0 Python foundations](b0/README.md) when learners need the language
subset used by the later snippets. Its numbered files use only the standard
library; an optional FastAPI example is separate.

Explore B1–B3 more deeply in the [Jupyter notebooks](../notebooks/README.md):
tokens/messages, tool contracts/execution, and workflows/state/approval.
The notebooks contain complete experiments; the short snippets remain the
smallest teaching illustrations.

| Module | Core teaching purpose | Core files | Guide |
| --- | --- | ---: | --- |
| B0 · preparation | Core Python and a follow-on application bridge | 14 | [Teaching map](b0/README.md) |
| B1 | Model access, conversations, tokens and operating cost | 6 | [Teaching map](b1/README.md) |
| B2 | Functions, tool-using agents, frameworks and shared MCP tools | 5 | [Teaching map](b2/README.md) |
| B3 | Multi-step autonomy, delegation, state and human review | 6 | [Teaching map](b3/README.md) |
| B4 | Enterprise data and governed reads | 3 | [Teaching map](b4/README.md) |
| B6 | RAG, retrieval repairs and agentic RAG | 7 | [Teaching map](b6/README.md) |
| B5 | Evaluation, tracing and improvement | 3 | [Teaching map](b5/README.md) |

Teach in order B1, B2, B3, B4, B6, B5. B2's five files represent four teaching steps because MCP uses a server/client pair. B1–B3 extensions and references are excluded from the core counts.

## B1–B3 folder convention

These modules use the same layout:

```text
b1/, b2/ or b3/
├── README.md          # setup, teaching order and run commands
├── requirements.txt   # module dependencies
├── 01_*.py            # core examples in teaching order
├── 02_*.py
├── ...
├── extensions/        # optional lab additions, numbered separately
└── reference/         # supporting examples without lesson numbers
```

Open the module README and follow its numbered root files. B1 and B3 run `01`–`06`; B2 runs `01`–`05`. B2's `04` is a server to leave running while executing client `05` in another terminal. B3's `06` pauses for a terminal reviewer decision. Each extension/reference folder has its own short guide.

## Teaching and execution

B1 begins with a general-knowledge chatbot and adds local model access, instructions, history, tokens and measurements. B2 adds an actual application capability, then changes how it is invoked and shared. Questions, instructions, unknown identifiers and other variations should usually be edits to the same example.

For B1–B3, run `uv sync --locked` once from track-b. Then use `uv run python ...` for every core example or extension; no environment activation is needed. Read [SETUP](../SETUP.md), then the module guide. B1–B3 use `OPEN_AI_KEY`; other modules and older references still use `OPENAI_API_KEY`. Store real credentials in an ignored `.env`, never in a script.

```bash
uv run python snippets/b1/01_openai_call.py
uv run python snippets/b1/02_ollama_call.py
uv run python snippets/b2/01_status_function.py
uv run python snippets/b2/02_openai_agent_with_tool.py
```

Model examples require real access. Deterministic examples label prepared inputs. A service failure is not replaced by fake model output. Use the [B1–B3 TODO labs](../labs/README.md) to apply the mechanisms in a standalone use case or the PortOps capstone; each supplies checkpoint commands and complete scaffolding around the unfinished learner functions.
