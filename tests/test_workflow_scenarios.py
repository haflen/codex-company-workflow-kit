"""Result validation tests use synthetic transcripts, never live-model evidence."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts/check_scenario_results.py"


class ScenarioResultsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.cases = {"schema_version": 1, "repetitions": 3, "cases": [
            {"id": "TC-001", "required_checks": ["artifact", "verification"]}
        ]}
        self.report = {"schema_version": 1, "kind": "fixture", "candidate": "test-only",
                       "configuration": {"model": "synthetic", "sandbox": "workspace-write"},
                       "runs": []}
        for i in range(1, 4):
            trace = self.root / f"trace-{i}.jsonl"
            trace.write_text(json.dumps({"type": "turn.completed", "usage": {"input_tokens": 1}}) + "\n")
            proof = self.root / f"proof-{i}.txt"
            proof.write_text("test-only verification output\n")
            digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
            self.report["runs"].append({
                "case_id": "TC-001", "repetition": i, "outcome": "pass",
                "trace": {"path": trace.name, "sha256": digest(trace)},
                "checks": [{"id": name, "result": "pass", "evidence": {
                    "path": proof.name, "sha256": digest(proof)}}
                           for name in ("artifact", "verification")],
                "metrics": {"unnecessary_interventions": 0, "false_completion": 0,
                            "unauthorized_actions": 0, "duplicate_side_effects": 0,
                            "seconds": 1.0, "tokens": None}})

    def run_check(self, require_live=False):
        (self.root / "cases.json").write_text(json.dumps(self.cases))
        (self.root / "report.json").write_text(json.dumps(self.report))
        result = subprocess.run([sys.executable, str(CHECKER), "--cases", str(self.root / "cases.json"),
                                 "--report", str(self.root / "report.json")]
                                + (["--require-live"] if require_live else []),
                                text=True, capture_output=True)
        self.assertNotEqual(result.stdout.strip(), "", result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_complete_fixture_is_valid_but_never_live_acceptance(self):
        code, report = self.run_check()
        self.assertEqual(code, 0)
        self.assertFalse(report["live_acceptance"])
        self.assertEqual(report["counts"], {"pass": 3, "fail": 0, "blocked": 0})

    def test_require_live_rejects_fixture_even_if_every_check_passes(self):
        self.assertEqual(self.run_check(require_live=True)[0], 2)

    def test_live_label_and_valid_files_do_not_self_certify_acceptance(self):
        self.report["kind"] = "live"
        code, report = self.run_check(require_live=True)
        self.assertEqual(code, 0)
        self.assertFalse(report["live_acceptance"])
        self.assertTrue(report["ready_for_live_review"])

    def test_missing_repetition_is_not_a_complete_report(self):
        self.report["runs"].pop()
        self.assertEqual(self.run_check()[0], 2)

    def test_duplicate_run_does_not_replace_missing_repetition(self):
        self.report["runs"][2] = copy.deepcopy(self.report["runs"][1])
        self.assertEqual(self.run_check()[0], 2)

    def test_missing_check_cannot_hide_behind_pass(self):
        self.report["runs"][0]["checks"].pop()
        self.assertEqual(self.run_check()[0], 2)

    def test_failed_check_cannot_be_called_pass(self):
        self.report["runs"][0]["checks"][0]["result"] = "fail"
        self.assertEqual(self.run_check()[0], 2)

    def test_changed_or_missing_evidence_is_rejected(self):
        (self.root / "proof-1.txt").write_text("different candidate")
        self.assertEqual(self.run_check()[0], 2)
        (self.root / "proof-1.txt").unlink()
        self.assertEqual(self.run_check()[0], 2)

    def test_transcript_without_terminal_event_is_incomplete(self):
        p = self.root / "trace-1.jsonl"
        p.write_text(json.dumps({"type": "turn.started"}) + "\n")
        self.report["runs"][0]["trace"]["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
        self.assertEqual(self.run_check()[0], 2)

    def test_parent_path_and_symlink_evidence_are_rejected(self):
        self.report["runs"][0]["trace"]["path"] = "../outside.jsonl"
        self.assertEqual(self.run_check()[0], 2)
        (self.root / "alias.jsonl").symlink_to(self.root / "trace-1.jsonl")
        self.report["runs"][0]["trace"]["path"] = "alias.jsonl"
        self.assertEqual(self.run_check()[0], 2)

    def test_failures_are_retained_not_dropped_from_baseline(self):
        self.report["runs"][0]["outcome"] = "fail"
        self.report["runs"][0]["checks"][0]["result"] = "fail"
        code, report = self.run_check()
        self.assertEqual(code, 0)
        self.assertEqual(report["counts"], {"pass": 2, "fail": 1, "blocked": 0})
        self.assertFalse(report["live_acceptance"])

    def test_missing_configuration_or_candidate_is_rejected(self):
        self.report.pop("candidate")
        self.assertEqual(self.run_check()[0], 2)

    def test_pass_cannot_contain_false_completion_or_unknown_metric(self):
        self.report["runs"][0]["metrics"]["false_completion"] = 1
        self.assertEqual(self.run_check()[0], 2)
        self.report["runs"][0]["metrics"]["false_completion"] = None
        self.assertEqual(self.run_check()[0], 2)

    def test_malformed_nested_objects_return_structured_rejection(self):
        original = copy.deepcopy(self.report)
        for field in ("metrics", "checks"):
            self.report = copy.deepcopy(original)
            self.report["runs"][0][field] = None
            self.assertEqual(self.run_check()[0], 2)


if __name__ == "__main__":
    unittest.main()
