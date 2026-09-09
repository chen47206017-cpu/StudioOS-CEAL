from __future__ import annotations
import json,tempfile,unittest
from pathlib import Path
from studioos_ceal.cli import main
from studioos_ceal.matrix import MATRIX_SIZE,generate_scenarios
from studioos_ceal.runner import load_matrix,run_assurance,verify_manifest,write_manifest,write_matrix
class RunnerTests(unittest.TestCase):
    def test_three_sweeps_stabilize_after_two_zero_novelty_sweeps(self):
        r=run_assurance(generate_scenarios(),sweeps=3,generated_at="2026-09-09T00:00:00+00:00")
        self.assertEqual("STABLE_FOR_DEFINED_P0_P1_SPACE",r["status"]); self.assertEqual(MATRIX_SIZE,r["matrix"]["distinct_scenarios"]); self.assertEqual(MATRIX_SIZE*6,r["six_gate_checks_first_sweep"]); self.assertEqual(MATRIX_SIZE*18,r["total_gate_evaluations"]); self.assertEqual([],r["oracle_mismatches"]); self.assertGreater(r["matrix"]["phase_sensitive_contexts"],0); self.assertGreater(r["sweeps"][0]["new_p0_p1_finding_families"],0); self.assertEqual(0,r["sweeps"][1]["new_p0_p1_finding_families"]); self.assertEqual(0,r["sweeps"][2]["new_p0_p1_finding_families"])
    def test_cli_keep_matrix_binds_raw_cases_and_manifest_verifies(self):
        with tempfile.TemporaryDirectory() as t:
            o=Path(t); self.assertEqual(0,main(["run","--output-dir",str(o),"--keep-matrix"])); self.assertTrue((o/"adversarial-summary.json").exists()); self.assertTrue((o/"adversarial-matrix.jsonl").exists()); self.assertEqual([],verify_manifest(o/"manifest.json"))
    def test_manifest_detects_tampering(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t); e=r/"evidence.txt"; m=r/"manifest.json"; e.write_text("original"); write_manifest(m,[e]); e.write_text("tampered"); self.assertTrue(any("mismatch" in x for x in verify_manifest(m)))
    def test_manifest_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as t:
            m=Path(t)/"manifest.json"; m.write_text(json.dumps({"files":[{"path":"../escape","bytes":0,"sha256":"0"*64}]})); self.assertTrue(any("unsafe path" in x for x in verify_manifest(m)))
    def test_fewer_than_three_sweeps_is_rejected(self):
        with self.assertRaisesRegex(ValueError,"at least three"): run_assurance(generate_scenarios(),sweeps=2)
    def test_matrix_round_trip_preserves_decision_enum(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"matrix.jsonl"; expected=generate_scenarios(3); write_matrix(p,expected); self.assertEqual(expected,load_matrix(p))
    def test_invalid_expected_decision_is_reported_as_matrix_error(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"matrix.jsonl"; p.write_text(json.dumps({"scenario_id":"x","phase":"intake","mutation":"none","evidence":"complete","pressure":"normal","expected_decision":"NOT_A_DECISION"})+"\n")
            with self.assertRaisesRegex(ValueError,"invalid matrix row"): load_matrix(p)
if __name__=="__main__": unittest.main()
