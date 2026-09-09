from __future__ import annotations
import unittest
from studioos_ceal.engine import PolicyEngine
from studioos_ceal.matrix import generate_scenarios
from studioos_ceal.models import Decision,Scenario
class EngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.engine=PolicyEngine()
    def test_all_scenarios_match_explicit_oracle(self):
        mismatches=[]
        for s in generate_scenarios():
            actual=self.engine.evaluate(s).decision
            if actual!=s.expected_decision: mismatches.append((s.scenario_id,s.expected_decision,actual))
        self.assertEqual([],mismatches)
    def test_phase_dimension_changes_evidence_decision(self):
        a=Scenario("phase-intake","intake","none","missing_runtime","normal",Decision.ALLOW)
        b=Scenario("phase-runtime","runtime_verify","none","missing_runtime","normal",Decision.HOLD)
        self.assertEqual(Decision.ALLOW,self.engine.evaluate(a).decision); self.assertEqual(Decision.HOLD,self.engine.evaluate(b).decision)
    def test_frozen_policy_drift_blocks(self):
        s=Scenario("policy-drift","implementation","policy_drift","complete","normal",Decision.BLOCK); r=self.engine.evaluate(s)
        self.assertEqual(Decision.BLOCK,r.decision); self.assertIn("contract:POLICY_DRIFT:BLOCK:P0",r.high_priority_families)
    def test_audit_rule_self_modification_blocks(self):
        s=Scenario("audit-self-mod","audit","audit_rule_self_modification","complete","deadline",Decision.BLOCK)
        self.assertEqual(Decision.BLOCK,self.engine.evaluate(s).decision)
    def test_safe_complete_change_is_allowed(self):
        s=Scenario("manual-safe","implementation","none","complete","normal",Decision.ALLOW); r=self.engine.evaluate(s)
        self.assertEqual(Decision.ALLOW,r.decision); self.assertEqual(6,len(r.gate_results))
if __name__=="__main__": unittest.main()
