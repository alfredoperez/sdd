#!/usr/bin/env python3
"""
Tests for drain-spec-context.py. Run from the repo root:

  python3 -m unittest discover -s lib/scripts -p 'test_*.py'

No third-party deps — stdlib unittest only.
"""
import importlib.util
import json
import os
import tempfile
import unittest


# Load the hyphenated module by path.
_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "drain_spec_context", os.path.join(_HERE, "drain-spec-context.py")
)
drain_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(drain_mod)


def write_json(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f)


def write_journal(path, events):
    with open(path, "w") as f:
        for e in events:
            f.write(json.dumps(e) + "\n")


def read_json(path):
    with open(path) as f:
        return json.load(f)


class DrainTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.json_path = os.path.join(self.dir, ".spec-context.json")
        self.journal_path = os.path.join(self.dir, ".spec-context.events.jsonl")

    def base_ctx(self, **extra):
        ctx = {
            "workflow": "sdd",
            "currentStep": "implement",
            "specName": "Demo",
            "createdAt": "2026-05-21T10:00:00Z",
            "transitions": [],
        }
        ctx.update(extra)
        return ctx

    def test_folds_events_into_state(self):
        write_json(self.json_path, self.base_ctx())
        write_journal(self.journal_path, [
            {"seq": 1, "at": "2026-05-21T12:00:00.001Z", "kind": "task_done",
             "step": "implement", "substep": "phase1",
             "from": {"step": "implement", "substep": "phase1"},
             "set": {"task_summaries.T001": {"status": "DONE", "did": "did a",
                                             "files": ["a.ts"], "concerns": []},
                     "currentTask": "T002", "last_action": "T001 done"},
             "union": {"files_modified": ["a.ts"]}},
            {"seq": 2, "at": "2026-05-21T12:00:05.123Z", "kind": "task_done",
             "step": "implement", "substep": "phase1",
             "from": {"step": "implement", "substep": "phase1"},
             "set": {"task_summaries.T002": {"status": "DONE_WITH_CONCERNS",
                                             "did": "did b", "files": ["b.ts", "a.ts"],
                                             "concerns": ["edge case"]},
                     "currentTask": None, "last_action": "T002 done"},
             "union": {"files_modified": ["b.ts", "a.ts"]},
             "append": {"decisions": ["chose X"],
                        "concerns": [{"task": "T002", "note": "edge case"}]}},
        ])

        rc = drain_mod.drain(self.dir)
        self.assertEqual(rc, 0)
        ctx = read_json(self.json_path)

        # Field updates folded.
        self.assertEqual(ctx["task_summaries"]["T001"]["did"], "did a")
        self.assertEqual(ctx["task_summaries"]["T002"]["status"], "DONE_WITH_CONCERNS")
        self.assertIsNone(ctx["currentTask"])
        self.assertEqual(ctx["last_action"], "T002 done")
        # union dedups, preserves first-seen order.
        self.assertEqual(ctx["files_modified"], ["a.ts", "b.ts"])
        # append.
        self.assertEqual(ctx["decisions"], ["chose X"])
        self.assertEqual(ctx["concerns"], [{"task": "T002", "note": "edge case"}])
        # one transition per event, in seq order, with carried from/at.
        self.assertEqual(len(ctx["transitions"]), 2)
        self.assertEqual([t["at"] for t in ctx["transitions"]],
                         ["2026-05-21T12:00:00.001Z", "2026-05-21T12:00:05.123Z"])
        self.assertTrue(all(t["by"] == "sdd" for t in ctx["transitions"]))
        # watermark advanced.
        self.assertEqual(ctx["drainedSeq"], 2)

    def test_idempotent_redrain(self):
        write_json(self.json_path, self.base_ctx())
        write_journal(self.journal_path, [
            {"seq": 1, "at": "2026-05-21T12:00:00.001Z", "step": "implement",
             "substep": "phase1", "from": None, "set": {"progress": "phase1"}},
        ])
        self.assertEqual(drain_mod.drain(self.dir), 0)
        first = read_json(self.json_path)
        # Re-draining the same journal must not double-append the transition.
        self.assertEqual(drain_mod.drain(self.dir), 0)
        second = read_json(self.json_path)
        self.assertEqual(len(first["transitions"]), 1)
        self.assertEqual(len(second["transitions"]), 1)
        self.assertEqual(second["drainedSeq"], 1)

    def test_preserves_foreign_fields(self):
        # Extension-owned fields + a foreign transition must survive a fold.
        write_json(self.json_path, self.base_ctx(
            status="active",
            stepHistory={"specify": {"startedAt": "2026-05-21T10:00:00Z",
                                     "completedAt": "2026-05-21T10:05:00Z"}},
            transitions=[{"step": "specify", "substep": None, "from": None,
                          "by": "extension", "at": "2026-05-21T10:00:00Z"}],
        ))
        write_journal(self.journal_path, [
            {"seq": 1, "at": "2026-05-21T12:00:00.001Z", "step": "implement",
             "substep": "phase1", "from": None, "set": {"progress": "phase1"}},
        ])
        drain_mod.drain(self.dir)
        ctx = read_json(self.json_path)
        self.assertEqual(ctx["status"], "active")
        self.assertIn("specify", ctx["stepHistory"])
        # foreign extension transition preserved, SDD one appended after it.
        self.assertEqual(len(ctx["transitions"]), 2)
        self.assertEqual(ctx["transitions"][0]["by"], "extension")
        self.assertEqual(ctx["transitions"][1]["by"], "sdd")

    def test_resume_only_folds_new_events(self):
        # Simulate a partially-drained spec: drainedSeq=2, journal has 1..3.
        write_json(self.json_path, self.base_ctx(drainedSeq=2, transitions=[
            {"step": "implement", "substep": "phase1", "from": None,
             "by": "sdd", "at": "2026-05-21T12:00:00.001Z"},
            {"step": "implement", "substep": "phase1", "from": None,
             "by": "sdd", "at": "2026-05-21T12:00:01.001Z"},
        ]))
        write_journal(self.journal_path, [
            {"seq": 1, "at": "2026-05-21T12:00:00.001Z", "step": "implement",
             "substep": "phase1", "from": None, "set": {"progress": "phase1"}},
            {"seq": 2, "at": "2026-05-21T12:00:01.001Z", "step": "implement",
             "substep": "phase1", "from": None, "set": {"progress": "phase1"}},
            {"seq": 3, "at": "2026-05-21T12:00:02.001Z", "step": "implement",
             "substep": "hooks", "from": {"step": "implement", "substep": "phase1"},
             "set": {"progress": "hooks"}},
        ])
        drain_mod.drain(self.dir)
        ctx = read_json(self.json_path)
        self.assertEqual(ctx["drainedSeq"], 3)
        self.assertEqual(ctx["progress"], "hooks")
        # only seq 3 appended (2 pre-existing + 1 new).
        self.assertEqual(len(ctx["transitions"]), 3)

    def test_nested_set_paths(self):
        write_json(self.json_path, self.base_ctx())
        write_journal(self.journal_path, [
            {"seq": 1, "at": "2026-05-21T12:00:00.001Z", "step": "specify",
             "substep": "writing-spec", "from": None,
             "set": {"step_summaries.specify": {"complexity": "normal",
                                                "requirements": 3, "scenarios": 2,
                                                "key_finding": "uses managers"}}},
        ])
        drain_mod.drain(self.dir)
        ctx = read_json(self.json_path)
        self.assertEqual(ctx["step_summaries"]["specify"]["requirements"], 3)

    def test_no_journal_is_noop(self):
        write_json(self.json_path, self.base_ctx())
        self.assertEqual(drain_mod.drain(self.dir), 0)
        # File unchanged (no drainedSeq added).
        self.assertNotIn("drainedSeq", read_json(self.json_path))

    def test_init_when_json_missing(self):
        # Journal exists but no JSON yet — drain still folds (defensive).
        write_journal(self.journal_path, [
            {"seq": 1, "at": "2026-05-21T12:00:00.001Z", "step": "implement",
             "substep": "phase1", "from": None, "set": {"progress": "phase1"}},
        ])
        drain_mod.drain(self.dir)
        ctx = read_json(self.json_path)
        self.assertEqual(ctx["progress"], "phase1")
        self.assertEqual(ctx["drainedSeq"], 1)


if __name__ == "__main__":
    unittest.main()
