"""Instructor checks for supplied B4/B5 scaffolding, not learner answers."""

import asyncio
import contextlib
import importlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from sqlalchemy import inspect, text
from sqlalchemy.exc import DatabaseError

LAB = Path(__file__).resolve().parents[1] / "container_help_desk"
sys.path.insert(0, str(LAB))


class NewLabChecks(unittest.TestCase):
    def test_help_and_unfinished_checkpoints_work_without_model_access(self):
        for module, checkpoint, todo in [("b4", "read", "TODO B4.2"),
                                          ("b5", "baseline", "TODO B5.1")]:
            help_run = subprocess.run([sys.executable, str(LAB / f"{module}.py"), "--help"],
                                      cwd=tempfile.gettempdir(), capture_output=True, text=True)
            self.assertEqual(help_run.returncode, 0, help_run.stderr)
            unfinished = subprocess.run([sys.executable, str(LAB / f"{module}.py"), checkpoint],
                                       cwd=tempfile.gettempdir(), capture_output=True, text=True)
            self.assertEqual(unfinished.returncode, 2, unfinished.stderr)
            self.assertIn(todo, unfinished.stdout)
            self.assertNotIn("ANSWER:", unfinished.stdout)

    def test_projection_omits_other_owner_and_private_columns(self):
        data = importlib.import_module("b4_data")
        source, snapshot = data.make_databases()
        try:
            with source.connect() as connection:
                self.assertEqual(connection.execute(text("SELECT fee FROM container_fees WHERE container_id='C2'")).scalar_one(), 200)
            with snapshot.connect() as connection:
                self.assertEqual(connection.execute(text("SELECT container_id, fee FROM container_fees ORDER BY container_id")).fetchall(),
                                 [("C1", 100), ("C4", 50), ("C5", 75)])
                self.assertEqual(connection.execute(text("SELECT container_id FROM events ORDER BY container_id")).fetchall(),
                                 [("C1",), ("C1",), ("C4",)])
            columns = {column["name"] for column in inspect(snapshot).get_columns("container_fees")}
            self.assertNotIn("owner", columns)
            self.assertNotIn("private_note", columns)
        finally:
            source.dispose(); snapshot.dispose()

    def test_database_policy_rejects_writes_private_reads_and_policy_changes(self):
        data = importlib.import_module("b4_data")
        source, snapshot = data.make_databases()
        try:
            data.restrict_database(snapshot)
            with snapshot.connect() as connection:
                for sql in ["DELETE FROM container_fees", "SELECT * FROM private_contacts",
                            "SELECT * FROM events", "ATTACH DATABASE ':memory:' AS other",
                            "PRAGMA query_only=OFF"]:
                    with self.subTest(sql=sql), self.assertRaises(DatabaseError):
                        connection.execute(text(sql)).fetchall()
                self.assertEqual(connection.execute(text("SELECT SUM(fee) FROM container_fees WHERE status='delayed'")).scalar_one(), 150)
                aliases=list("abcdefghijkl")
                heavy="SELECT a.container_id FROM "+" CROSS JOIN ".join("container_fees "+a for a in aliases)+" ORDER BY "+" + ".join(a+".fee" for a in aliases)
                with self.assertRaisesRegex(DatabaseError, "interrupted"):
                    connection.execute(text(heavy)).fetchmany(3)
        finally:
            source.dispose(); snapshot.dispose()

    def test_query_failure_does_not_become_an_empty_or_zero_result(self):
        lab = importlib.import_module("b4")
        with self.assertRaises(RuntimeError):
            lab.unpack_response(SimpleNamespace(metadata={"sql_query": "DELETE FROM container_fees"}))
        empty = lab.unpack_response(SimpleNamespace(metadata={"sql_query":"SELECT fee", "result":[], "col_keys":["fee"]}))
        null = lab.unpack_response(SimpleNamespace(metadata={"sql_query":"SELECT SUM(fee)", "result":[(None,)], "col_keys":["SUM(fee)"]}))
        self.assertEqual(empty["rows"], [])
        self.assertEqual(null["rows"], [[None]])

    def test_final_text_without_a_tool_observation_cannot_pass(self):
        lab = importlib.import_module("b5")
        case={"name":"boundary", "caller":"A", "container_id":"C2", "unavailable":False,
              "expected_fee":200, "expected_decision":"review"}
        # Replace only external execution and unfinished learner hooks. The supplied
        # observation/ID/stop checks run for real and must reject ungrounded text.
        result=SimpleNamespace(final_output="review", context_wrapper=SimpleNamespace(usage=SimpleNamespace(input_tokens=0,output_tokens=0)))
        with patch.object(lab,"make_agent",return_value=object()), patch.object(lab,"configure_sdk"), \
             patch.object(lab.Runner,"run_sync",return_value=result), patch.object(lab,"grade_observation",return_value=True):
            first=lab.run_trial(case,False,4)
            second=lab.run_trial(case,False,4)
            self.assertEqual(first["calls"], [])
            self.assertEqual(second["calls"], [])
            self.assertIsNone(first["observation"])
            self.assertFalse(lab.trial_passed(case,first))

    def test_every_stopped_trial_remains_in_the_repeated_result(self):
        lab=importlib.import_module("b5")
        from agents import MaxTurnsExceeded
        case={"name":"boundary", "caller":"A", "container_id":"C2", "unavailable":False,
              "expected_fee":200, "expected_decision":"review"}
        with patch.object(lab,"make_agent",return_value=object()), patch.object(lab,"configure_sdk"), \
             patch.object(lab.Runner,"run_sync",side_effect=MaxTurnsExceeded("test turn bound")):
            with contextlib.redirect_stdout(io.StringIO()):
                trials=lab.repeat_cases([case],False,2,1)
        self.assertEqual(len(trials),2)
        self.assertTrue(all(trial["error"]["type"]=="MaxTurnsExceeded" for trial in trials))
        self.assertTrue(all(not trial["passed"] for trial in trials))


if __name__ == "__main__":
    unittest.main()
