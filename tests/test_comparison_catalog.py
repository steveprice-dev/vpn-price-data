import copy
import json
import sys
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_comparison_catalog import comparison_checks

class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.feed = json.loads((ROOT / "tests/fixtures/comparison-catalog.json").read_text())
        self.schema = Draft202012Validator(json.loads((ROOT / "schemas/comparison-catalog.schema.json").read_text()), format_checker=FormatChecker())

    def test_fixture_and_source_identity(self):
        self.schema.validate(self.feed)
        self.assertEqual(comparison_checks(self.feed, {"cyberghost"}), [])
        self.feed["records"][0]["source_url"] = "https://example.com/other"
        self.assertTrue(comparison_checks(self.feed, {"cyberghost"}))

    def test_invalid_economics_freshness_and_private_fields(self):
        for update in [{"service_months": 5}, {"effective_intro_monthly": 100}, {"renewal_total_status": "not_applicable"}, {"observed_at": "2026-01-01T00:00:00Z"}, {"materially_changed_at": "2027-01-01T00:00:00Z"}, {"source_url": "https://example.com/?token=private"}]:
            feed = copy.deepcopy(self.feed)
            feed["records"][0].update(update)
            with self.subTest(update=update): self.assertTrue(comparison_checks(feed, {"cyberghost"}))
        self.feed["records"][0]["evidence_path"] = "private/path"
        self.assertTrue(list(self.schema.iter_errors(self.feed)))

    def test_duplicate_and_registry_exclusion(self):
        self.assertTrue(comparison_checks(self.feed, set()))
        self.feed["records"].append(copy.deepcopy(self.feed["records"][0]))
        self.assertTrue(comparison_checks(self.feed, {"cyberghost"}))
