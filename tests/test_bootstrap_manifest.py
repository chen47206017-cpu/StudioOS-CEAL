from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]


class BootstrapManifestTests(unittest.TestCase):
    def test_manifest_matches_exact_repository_payload_bytes(self) -> None:
        manifest = json.loads((ROOT / "BOOTSTRAP_MANIFEST.json").read_text(encoding="utf-8"))
        records = manifest["files"]
        self.assertEqual(manifest["file_count"], len(records))
        self.assertEqual(len(records), len({record["path"] for record in records}))
        for record in records:
            rel = record["path"]
            parts = PurePosixPath(rel).parts
            self.assertFalse(rel.startswith("/"))
            self.assertNotIn("..", parts)
            target = (ROOT / rel).resolve()
            target.relative_to(ROOT.resolve())
            self.assertTrue(target.is_file(), rel)
            data = target.read_bytes()
            self.assertEqual(record["size"], len(data), rel)
            self.assertEqual(record["sha256"], hashlib.sha256(data).hexdigest(), rel)


if __name__ == "__main__":
    unittest.main()
