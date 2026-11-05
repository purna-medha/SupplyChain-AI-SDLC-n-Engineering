# Run B1–B3

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) once. Run these steps from the **track-b** folder.

1. **Install packages.**

   ```bash
   uv sync --locked
   ```

   This prepares Python 3.12 and the shared environment. No activation is needed.

2. **Create snippets/.env** with your OpenAI API key.

   ```dotenv
   OPEN_AI_KEY=your-key-here
   ```

   Older reference examples also need OPENAI_API_KEY set to the same key.

3. **Run your first model call.**

   ```bash
   uv run python snippets/b1/01_openai_call.py
   ```

   **Success:** an answer, token counts and estimated cost appear.

For another example, replace the script path after **uv run python**.

## When needed

- **Local model:** [Ollama setup](snippets/b1/README.md#setup-and-execution).
- **Shared tools:** [MCP server and client](snippets/b2/README.md#setup).
- **Labs or notebooks:** follow their [lab](labs/README.md) or [notebook](notebooks/README.md) setup.
- **B4–B6:** use a separate environment with [teaching requirements](requirements-teaching.txt); B6 also needs [RAG requirements](requirements-rag.txt).

Keep other environments separate from the locked B1–B3 environment.

[Package versions and setup verification](docs/uv-setup-verification.md).
