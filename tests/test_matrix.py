from __future__ import annotations

import hashlib
import json
import unittest

from studioos_ceal.matrix import MATRIX_SIZE, generate_scenarios


class MatrixTests(unittest.TestCase):
    def test_full_matrix_has_exactly_8000_unique_scenarios(self) -> None:
        scenarios = generate_scenarios()
        self.assertEqual(8000, MATRIX_SIZE)
        self.assertEqual(MATRIX_SIZE, len(scenarios))
        self.assertEqual(MATRIX_SIZE, len({item.scenario_id for item in scenarios}))
        self.assertEqual(
            MATRIX_SIZE,
            len(
                {
                    (item.phase, item.mutation, item.evidence, item.pressure)
                    for item in scenarios
                }
            ),
        )

    def test_generation_is_deterministic(self) -> None:
        def digest() -> str:
            rows = [
                json.dumps(item.as_dict(), ensure_ascii=False, sort_keys=True)
                for item in generate_scenarios()
            ]
            return hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()

        self.assertEqual(digest(), digest())

    def test_invalid_limit_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            generate_scenarios(0)
        with self.assertRaises(ValueError):
            generate_scenarios(MATRIX_SIZE + 1)


if __name__ == "__main__":
    unittest.main()
