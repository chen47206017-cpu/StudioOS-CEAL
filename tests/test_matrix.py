from __future__ import annotations
import hashlib,json,unittest
from studioos_ceal.matrix import MATRIX_SIZE,generate_scenarios
class MatrixTests(unittest.TestCase):
    def test_full_matrix_has_at_least_8000_unique_scenarios(self):
        s=generate_scenarios(); self.assertGreaterEqual(MATRIX_SIZE,8000); self.assertEqual(MATRIX_SIZE,len(s)); self.assertEqual(MATRIX_SIZE,len({x.scenario_id for x in s})); self.assertEqual(MATRIX_SIZE,len({(x.phase,x.mutation,x.evidence,x.pressure) for x in s}))
    def test_generation_is_deterministic(self):
        def d(): return hashlib.sha256("\n".join(json.dumps(x.as_dict(),ensure_ascii=False,sort_keys=True) for x in generate_scenarios()).encode()).hexdigest()
        self.assertEqual(d(),d())
    def test_invalid_limit_is_rejected(self):
        with self.assertRaises(ValueError): generate_scenarios(0)
        with self.assertRaises(ValueError): generate_scenarios(MATRIX_SIZE+1)
if __name__=="__main__": unittest.main()
