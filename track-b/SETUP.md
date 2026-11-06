# Run the teaching examples

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) once. Run these steps from **track-b**. See the [course map](README.md) for module order and status.

1. **Install B1–B5 packages.**

   ```bash
   uv sync --locked
   ```

   This prepares Python 3.12 and the shared environment. No activation is needed.

2. **Create snippets/.env** with your key.

   ```dotenv
   OPEN_AI_KEY=your-key-here
   ```

3. **Run your first call.**

   ```bash
   uv run python snippets/b1/01_openai_call.py
   ```

   **Success:** an answer, token counts and estimated cost appear. Replace the script path for another example.

## When needed

- **B0:** Python 3.11+ only; [first command](snippets/b0/README.md).
- **Local model:** [Ollama preparation](snippets/b1/README.md#before-the-local-example).
- **Shared tools:** [MCP in two terminals](snippets/b2/README.md#run-mcp-in-two-terminals).
- **Labs/notebooks:** use their separate [lab](labs/container_help_desk/README.md#prepare-once) or [notebook](notebooks/README.md#prepare-the-notebook-environment) environment.

## Later modules

B6 uses a separate environment from the locked B1–B5 environment:

```bash
uv venv .venv-later
source .venv-later/bin/activate
uv pip install -r requirements-teaching.txt
```

Also run `uv pip install -r requirements-rag.txt`. B6 examples and older references read **OPENAI_API_KEY**; add that variable to `snippets/.env` with the same key. Run their documented `python snippets/...` commands with this environment active.

B5 uses `OPEN_AI_KEY` and the shared environment. Its run guide separates offline examples from examples needing actual model access. No observability account or MCP server is required. See the [B5 run guide](snippets/b5/README.md) and [verification record](snippets/b5/VERIFICATION.md).

B4 also uses the shared environment and `OPEN_AI_KEY`. Its six core examples build their own disposable databases; no server is needed. Four run offline, while the question-to-SQL and agent examples make actual model calls. See the [B4 run guide](snippets/b4/README.md). Earlier API and reviewed-write demonstrations remain optional references.
