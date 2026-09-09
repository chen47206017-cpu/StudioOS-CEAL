from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from studioos_ceal.cli import main
from studioos_ceal.matrix import generate_scenarios
from studioos_ceal.runner import load_matrix, run_assurance, write_matrix


class RunnerTests(unittest.TestCase):
    def test_three_sweeps_converge_after_two_zero_novelty_sweeps(self) -> None:
        report = run_assurance(
            generate_scenarios(),
            sweeps=3,
            generated_at="2026-09-09T00:00:00+00:00",
        )
        self.assertEqual("CONVERGED_FOR_P0_P1", report["status"])
        self.assertEqual(8000, report["matrix"]["distinct_scenarios"])
        self.assertEqual(48000, report["six_gate_checks_first_sweep"])
        self.assertEqual(144000, report["total_gate_evaluations"])
        self.assertEqual([], report["oracle_mismatches"])
        self.assertGreater(report["sweeps"][0]["new_p0_p1_finding_families"], 0)
        self.assertEqual(0, report["sweeps"][1]["new_p0_p1_finding_families"])
        self.assertEqual(0, report["sweeps"][2]["new_p0_p1_finding_families"])

    def test_cli_writes_summary_and_manifest_without_committing_matrix(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            exit_code = main(["run", "--output-dir", str(output_dir)])
            self.assertEqual(0, exit_code)
            self.assertTrue((output_dir / "adversarial-summary.json").exists())
            self.assertTrue((output_dir / "manifest.json").exists())
            self.assertFalse((output_dir / "adversarial-matrix.jsonl").exists())
            summary = json.loads(
                (output_dir / "adversarial-summary.json").read_text(encoding="utf-8")
            )
            self.assertEqual("CONVERGED_FOR_P0_P1", summary["status"])

    def test_fewer_than_three_sweeps_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least three"):
            run_assurance(generate_scenarios(), sweeps=2)

    def test_matrix_round_trip_preserves_decision_enum(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "matrix.jsonl"
            expected = generate_scenarios(3)
            write_matrix(path, expected)
            actual = load_matrix(path)
            self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
