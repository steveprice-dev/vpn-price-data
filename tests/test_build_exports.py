import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_exports", ROOT / "scripts" / "build_exports.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class BuildExportsTests(unittest.TestCase):
    def test_empty_latest_has_header_only(self):
        snapshot = {"observations": []}
        text = MODULE.csv_text(snapshot)
        self.assertEqual(text.count("\n"), 1)
        self.assertTrue(text.startswith("observation_id,"))

    def test_columns_are_unique(self):
        self.assertEqual(len(MODULE.COLUMNS), len(set(MODULE.COLUMNS)))

    def test_empty_markdown_does_not_imply_results(self):
        text = MODULE.markdown_text({"observations": []})
        self.assertIn("No manually reviewed observations", text)
        self.assertNotIn("| Provider |", text)


if __name__ == "__main__":
    unittest.main()
