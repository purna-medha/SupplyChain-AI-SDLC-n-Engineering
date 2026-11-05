"""Supplied setup and file handling. Learners work in b1.py, b2.py and b3.py."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv

LAB = Path(__file__).resolve().parent
WORK = LAB / "work"
load_dotenv(LAB / ".env")
load_dotenv(LAB.parents[1] / ".env")
load_dotenv(LAB.parents[2] / ".env")


def configure_sdk():
    from agents import set_default_openai_key, set_tracing_disabled

    key = os.environ.get("OPEN_AI_KEY")
    if not key:
        raise ValueError("Set OPEN_AI_KEY in this lab's .env or export it before a model run.")
    set_default_openai_key(key)
    set_tracing_disabled(True)


def task_path(container_id):
    # The identifier is a filename component, not an arbitrary path.
    if not container_id or not all(c.isalnum() or c in "-_" for c in container_id):
        raise ValueError("Use a container identifier containing letters, digits, - or _.")
    WORK.mkdir(parents=True, exist_ok=True)
    return WORK / f"task-{container_id}.json"


def load_task(container_id):
    path = task_path(container_id)
    if not path.exists():
        raise ValueError("Run the investigate checkpoint for this container first.")
    state = json.loads(path.read_text(encoding="utf-8"))
    if state.get("container_id") != container_id or not state.get("draft"):
        raise ValueError("This task file does not contain this container's draft.")
    return state


def append_outbox(entry):
    WORK.mkdir(parents=True, exist_ok=True)
    path = WORK / "outbox.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    if entry not in rows:
        with path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(entry) + "\n")


def run_cli(main):
    """Make unfinished work visible without a long framework traceback."""
    try:
        main()
    except NotImplementedError as exc:
        print(f"{exc}\nCheckpoint unfinished. Implement that function and rerun.")
        raise SystemExit(2)
    except (ValueError, RuntimeError) as exc:
        print(f"STOP: {exc}")
        raise SystemExit(1)

