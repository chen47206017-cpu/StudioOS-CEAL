from __future__ import annotations
import unittest
from studioos_ceal.engine import PolicyEngine
from studioos_ceal.matrix import generate_scenarios
from studioos_ceal.models import Decision

class AdversarialInvariantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine=PolicyEngine(); cls.scenarios=generate_scenarios()
    def test_p0_mutations_never_degrade_below_block(self):
        p0={"secret_write","destructive_command","production_data_write","paid_external_call","evidence_tamper","audit_rule_self_modification","policy_drift","task_contract_drift"}
        self.assertEqual([], [s.scenario_id for s in self.scenarios if s.mutation in p0 and self.engine.evaluate(s).decision!=Decision.BLOCK])
    def test_scope_escape_never_allows(self):
        guarded={"out_of_scope_file","denied_file","dependency_drift","parallel_system","untracked_change_omission"}
        self.assertEqual([], [s.scenario_id for s in self.scenarios if s.mutation in guarded and self.engine.evaluate(s).decision==Decision.ALLOW])
    def test_contradictory_evidence_never_allows(self):
        self.assertEqual([], [s.scenario_id for s in self.scenarios if s.evidence in {"contradictory","side_effect"} and self.engine.evaluate(s).decision!=Decision.BLOCK])
    def test_deadline_never_weakens_a_hard_block(self):
        self.assertEqual([], [s.scenario_id for s in self.scenarios if s.pressure=="deadline" and s.mutation in {"secret_write","policy_drift","audit_rule_self_modification"} and self.engine.evaluate(s).decision!=Decision.BLOCK])

if __name__=="__main__": unittest.main()
