from __future__ import annotations
import copy,json,unittest
from pathlib import Path
from studioos_ceal.contracts import ContractError,validate_change_paths,validate_task_package
ROOT=Path(__file__).resolve().parents[1]
class ContractTests(unittest.TestCase):
    def setUp(self): self.package=json.loads((ROOT/"templates"/"TASK_PACKAGE.example.json").read_text(encoding="utf-8"))
    def test_example_is_valid(self): validate_task_package(self.package)
    def test_l4_is_valid(self): p=copy.deepcopy(self.package); p["risk_level"]="L4"; validate_task_package(p)
    def test_unknown_field_is_rejected(self):
        p=copy.deepcopy(self.package); p["surprise"]=True
        with self.assertRaisesRegex(ContractError,"unexpected fields"): validate_task_package(p)
    def test_invalid_contract_hash_is_rejected(self):
        p=copy.deepcopy(self.package); p["task_contract_sha256"]="abc"
        with self.assertRaisesRegex(ContractError,"64-hex"): validate_task_package(p)
    def test_denylist_takes_precedence(self):
        p=copy.deepcopy(self.package); p["scope"]["allow"].append("**")
        self.assertEqual(["secrets/token.txt: denied"],validate_change_paths(p,["secrets/token.txt"]))
    def test_outside_allowlist_is_rejected(self):
        p=copy.deepcopy(self.package); p["changed_paths"]=["random.txt"]
        with self.assertRaisesRegex(ContractError,"outside allowlist"): validate_task_package(p)
    def test_parent_traversal_is_rejected(self):
        p=copy.deepcopy(self.package); p["changed_paths"]=["../outside.txt"]
        with self.assertRaisesRegex(ContractError,"unsafe repository path"): validate_task_package(p)
    def test_windows_absolute_path_is_rejected(self):
        p=copy.deepcopy(self.package); p["changed_paths"]=[r"C:\production\secret.txt"]
        with self.assertRaisesRegex(ContractError,"unsafe repository path"): validate_task_package(p)
    def test_missing_stop_conditions_is_rejected(self):
        p=copy.deepcopy(self.package); p["stop_conditions"]=[]
        with self.assertRaisesRegex(ContractError,"stop_conditions"): validate_task_package(p)
    def test_closure_status_requires_discovered_complete_changeset(self):
        p=copy.deepcopy(self.package); p["status"]="TEST_PASS"
        with self.assertRaisesRegex(ContractError,"changeset_complete"): validate_task_package(p)
        p["changeset_complete"]=True
        with self.assertRaisesRegex(ContractError,"DISCOVERED_GIT"): validate_task_package(p)
        p["changeset_source"]="DISCOVERED_GIT"; validate_task_package(p)
if __name__=="__main__": unittest.main()
