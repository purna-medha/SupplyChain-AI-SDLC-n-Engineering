# Shared uv setup verification · 5 November 2026

The root pyproject.toml and uv.lock define one B1–B3 environment. The project is not installed as a Python package; the standalone teaching scripts continue to run directly.

## Environment and installation

- Verified with uv 0.8.9 and CPython 3.12.2 on macOS.
- The lockfile resolves 114 packages across its supported environments; the fresh Python 3.12 environment installed 108 distributions.
- A fresh temporary environment passed dependency compatibility checks. The existing project environment was also synchronized and passed compatibility checks.
- All 35 B1–B3 Python source files retained their baseline hashes.
- Locked versions satisfy the three module requirements files, retained for standalone installation.

## Measured setup

| Operation | Elapsed time |
| --- | ---: |
| fresh-sync | 16.466 s |
| warm-sync | 0.05 s |

These are wall-clock measurements on this machine with an existing package cache; the first sync still downloaded/prepared packages. They are not a cold-cache benchmark or a guarantee for participants' networks. The first combined library import also took about 17 seconds.

## Executed checks

| Check | Result |
| --- | --- |
| fresh-sync | PASS |
| warm-sync | PASS |
| dependency-check | PASS |
| runtime-imports | PASS |
| tokenizer | PASS |
| hosted-call | PASS |
| sdk-tool | PASS |
| llamaindex-tool | PASS |
| legacy-adapter | PASS |
| conversation-state | PASS |
| approval-rejected | PASS |
| Project-root uv run: tokenizer | PASS |
| Project-root uv run: B3 workflow | PASS |
| Final uv lock --check | PASS |
| Final project dependency check | PASS |

Representative hosted executions covered LiteLLM, OpenAI Agents SDK, LlamaIndex, the preserved OpenAI-compatible adapter, conversation/task state and a rejected approval with no outbox action. The tokenizer and deterministic workflow also ran through uv from the actual project root. The verification did not re-execute every snippet or reinstall Ollama.

The lockfile remained unchanged during the locked runs. Ollama, model downloads, credentials and each lab's separate setup remain outside Python dependency synchronization.
