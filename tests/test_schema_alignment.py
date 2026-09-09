from __future__ import annotations

import json
import unittest
from pathlib import Path

from studioos_ceal.contracts import ALLOWED_RISK_LEVELS, ALLOWED_STATUSES, REQUIRED_TOP_LEVEL

ROOT = Path(__file__).resolve().parents[1]


class SchemaAlignmentTests(unittest.TestCase):
    def test_task_package_schema_required_fields_match_runtime_validator(self) -> None:
        schema = json.loads((ROOT / "schemas" / "task-package.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(REQUIRED_TOP_LEVEL, set(schema["required"]))

    def test_task_package_schema_risk_and_status_cover_runtime_values(self) -> None:
        schema = json.loads((ROOT / "schemas" / "task-package.schema.json").read_text(encoding="utf-8"))
        props = schema["properties"]
        self.assertEqual(ALLOWED_RISK_LEVELS, set(props["risk_level"]["enum"]))
        self.assertEqual(ALLOWED_STATUSES, set(props["status"]["enum"]))


if __name__ == "__main__":
    unittest.main()
