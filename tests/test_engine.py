from __future__ import annotations

import unittest

from studioos_ceal.engine import PolicyEngine
from studioos_ceal.matrix import generate_scenarios
from studioos_ceal.models import Decision, Scenario


class EngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = PolicyEngine()

    def test_all_8000_scenarios_match_independent_oracle(self) -> None:
        mismatches = []
        for scenario in generate_scenarios():
            actual = self.engine.evaluate(scenario).decision
            if actual != scenario.expected_decision:
                mismatches.append((scenario.scenario_id, scenario.expected_decision, actual))
        self.assertEqual([], mismatches)

    def test_safe_complete_change_is_allowed(self) -> None:
        scenario = Scenario(
            scenario_id="manual-safe",
            phase="implementation",
            mutation="none",
            evidence="complete",
            pressure="normal",
            expected_decision=Decision.ALLOW,
        )
        result = self.engine.evaluate(scenario)
        self.assertEqual(Decision.ALLOW, result.decision)
        self.assertEqual(6, len(result.gate_results))

    def test_production_side_effect_is_fail_closed(self) -> None:
        scenario = Scenario(
            scenario_id="manual-risk",
            phase="runtime_verify",
            mutation="production_data_write",
            evidence="complete",
            pressure="deadline",
            expected_decision=Decision.BLOCK,
        )
        result = self.engine.evaluate(scenario)
        self.assertEqual(Decision.BLOCK, result.decision)
        self.assertIn(
            "risk:PRODUCTION_SIDE_EFFECT:BLOCK:P0",
            result.high_priority_families,
        )


if __name__ == "__main__":
    unittest.main()
