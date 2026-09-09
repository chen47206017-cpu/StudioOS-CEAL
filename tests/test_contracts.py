from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from studioos_ceal.contracts import ContractError, validate_change_paths, validate_task_package


ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = json.loads(
            (ROOT / "templates" / "TASK_PACKAGE.example.json").read_text(encoding="utf-8")
        )

    def test_example_is_valid(self) -> None:
        validate_task_package(self.package)

    def test_denylist_takes_precedence(self) -> None:
        package = copy.deepcopy(self.package)
        package["scope"]["allow"].append("**")
        errors = validate_change_paths(package, ["secrets/token.txt"])
        self.assertEqual(["secrets/token.txt: denied"], errors)

    def test_outside_allowlist_is_rejected(self) -> None:
        package = copy.deepcopy(self.package)
        package["changed_paths"] = ["random.txt"]
        with self.assertRaisesRegex(ContractError, "outside allowlist"):
            validate_task_package(package)

    def test_parent_traversal_is_rejected(self) -> None:
        package = copy.deepcopy(self.package)
        package["changed_paths"] = ["../outside.txt"]
        with self.assertRaisesRegex(ContractError, "unsafe repository path"):
            validate_task_package(package)

    def test_windows_absolute_path_is_rejected(self) -> None:
        package = copy.deepcopy(self.package)
        package["changed_paths"] = [r"C:\production\secret.txt"]
        with self.assertRaisesRegex(ContractError, "unsafe repository path"):
            validate_task_package(package)

    def test_missing_stop_conditions_is_rejected(self) -> None:
        package = copy.deepcopy(self.package)
        package["stop_conditions"] = []
        with self.assertRaisesRegex(ContractError, "stop_conditions"):
            validate_task_package(package)


if __name__ == "__main__":
    unittest.main()
