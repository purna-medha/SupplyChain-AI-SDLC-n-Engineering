"""Instructor checks for the supplied scaffolding, not learner TODO answers.

Run from the repository root: python -m unittest discover -s track-b/labs/tests -v
Dependencies: labs/container_help_desk/requirements.txt. No model key or network required.
"""

import importlib.util
import asyncio
import json
from itertools import product
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[3]
STANDALONE = ROOT / "track-b/labs/container_help_desk"


def load_file(directory, name):
    spec = importlib.util.spec_from_file_location(f"lab_{directory.name}_{name}", directory / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StarterChecks(unittest.TestCase):
    def test_modules_show_help_from_another_directory(self):
        for directory in (STANDALONE,):
            for name in ("b1", "b2", "b3"):
                with self.subTest(lab=directory.name, module=name):
                    result = subprocess.run(
                        [sys.executable, str(directory / f"{name}.py"), "--help"],
                        cwd=tempfile.gettempdir(), capture_output=True, text=True,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("usage:", result.stdout)

    def test_unfinished_model_call_names_the_todo_without_faking_a_reply(self):
        for directory in (STANDALONE,):
            result = subprocess.run(
                [sys.executable, str(directory / "b1.py"), "call"],
                cwd=tempfile.gettempdir(), capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("TODO B1.1", result.stdout)
            self.assertNotIn("REPLY:", result.stdout)

    def test_standalone_unknown_container_has_no_fee(self):
        records = load_file(STANDALONE, "records")
        self.assertIsNone(records.get_container("C9"))
        self.assertIsNone(records.get_demurrage("C9"))
        self.assertEqual(records.get_container("C1")["container_status_label"], "OVERDUE")
        self.assertEqual(records.get_demurrage("C1")["net_payable_demurrage_fee_usd"], 100)


    def test_local_outbox_keeps_the_reviewed_payload(self):
        for directory in (STANDALONE,):
            support = load_file(directory, "support")
            with tempfile.TemporaryDirectory() as temp:
                with patch.object(support, "WORK", Path(temp)):
                    entry = {"container_id": "C1", "text": "Review this exact text."}
                    support.append_outbox(entry)
                    support.append_outbox(entry)
                    entries = [json.loads(row) for row in (Path(temp) / "outbox.jsonl").read_text().splitlines()]
                    self.assertEqual(entries, [entry])

    def test_current_review_does_not_reuse_prior_outbox_membership(self):
        # Break caught: deriving this review from historical outbox membership.
        for directory, (decision, expected) in product((STANDALONE,), [("reject", "rejected"), ("approve", "incomplete")]):
            with self.subTest(lab=directory.name, decision=decision), tempfile.TemporaryDirectory() as temp:
                sys.path.insert(0, str(directory))
                try:
                    for name in ("support", "records"):
                        sys.modules.pop(name, None)
                    lab = load_file(directory, "b3")
                    support = sys.modules["support"]
                    work = Path(temp)
                    payload = {"container_id": "C1", "text": "The same saved draft."}
                    task = {"container_id": "C1", "draft": payload["text"], "findings": [], "review": "pending"}
                    (work / "task-C1.json").write_text(json.dumps(task))
                    (work / "outbox.jsonl").write_text(json.dumps(payload) + "\n")
                    interruption = SimpleNamespace(name="queue_customer_update", arguments=json.dumps(payload))
                    pending = SimpleNamespace(interruptions=[interruption], to_state=lambda: SimpleNamespace(to_json=lambda: {}))
                    resumed = SimpleNamespace(interruptions=[], final_output="Rejected.")

                    async def restore(*args):
                        return object()

                    # Replace model/runtime IO and the intentionally empty learner hooks.
                    # The scaffold's pending-payload checks and outcome file handling run for real.
                    with patch.object(support, "WORK", work), patch.object(lab, "WORK", work), \
                         patch.object(lab, "make_review_agent", return_value=object()), \
                         patch.object(lab, "configure_sdk"), patch.object(lab.Runner, "run", side_effect=[pending, resumed]), \
                         patch.object(lab.RunState, "from_json", side_effect=restore), \
                         patch.object(lab, "review_pending"), patch("builtins.input", return_value=decision), \
                         patch.object(lab, "save_task", side_effect=lambda state, path: path.write_text(json.dumps(state))):
                        asyncio.run(lab.run_review("C1"))
                    self.assertEqual(json.loads((work / "task-C1.json").read_text())["review"], expected)
                    self.assertEqual(len((work / "outbox.jsonl").read_text().splitlines()), 1)
                finally:
                    sys.path.pop(0)
                    for name in ("support", "records"):
                        sys.modules.pop(name, None)


if __name__ == "__main__":
    unittest.main()
