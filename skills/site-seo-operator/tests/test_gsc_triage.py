import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from gsc_triage import ExportError, Metric, read_export, render_report, review_flags


class GscTriageTests(unittest.TestCase):
    def make_csv(self, headers, rows):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        path = Path(root.name) / "gsc.csv"
        with path.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        return path

    def test_page_export_aliases_and_thousands(self):
        p = self.make_csv(["Top pages", "Clicks", "Impressions", "CTR", "Position"], [
            ["https://example.com/a", "47", "1,200", "3.9%", "12.5"]
        ])
        d = read_export(p, "page")
        self.assertEqual(d["https://example.com/a"].impressions, 1200)
        self.assertAlmostEqual(d["https://example.com/a"].ctr, 47 / 1200)

    def test_query_export(self):
        p = self.make_csv(["Top queries", "Clicks", "Impressions", "Position"], [["pdf file", "30", "200", "9.7"]])
        self.assertEqual(read_export(p, "query")["pdf file"].position, 9.7)

    def test_duplicate_dimension_fails(self):
        p = self.make_csv(["Page", "Clicks", "Impressions", "Position"], [["/x", 1, 50, 3], ["/x", 2, 50, 4]])
        with self.assertRaisesRegex(ExportError, "duplicate"):
            read_export(p, "page")

    def test_missing_column_fails(self):
        p = self.make_csv(["Page", "Clicks", "Position"], [["/x", 1, 3]])
        with self.assertRaisesRegex(ExportError, "Missing GSC column"):
            read_export(p, "page")

    def test_invalid_numbers_fails(self):
        p = self.make_csv(["Page", "Clicks", "Impressions", "Position"], [["/x", -1, 80, 3]])
        with self.assertRaises(ExportError):
            read_export(p, "page")
        p2 = self.make_csv(["Page", "Clicks", "Impressions", "Position"], [["/x", 1, 80, "nan"]])
        with self.assertRaises(ExportError):
            read_export(p2, "page")

    def test_position_8_to_20_and_threshold(self):
        self.assertIn("PAGE_2_REVIEW", review_flags(Metric("/x", 10, 100, 12.2), None))
        self.assertEqual(review_flags(Metric("/x", 1, 99, 12.2), None), [])

    def test_ctr_drop_at_stable_position(self):
        old = Metric("/x", 60, 1000, 5.0)
        now = Metric("/x", 20, 1000, 5.2)
        self.assertIn("CTR_DROP_REVIEW", review_flags(now, old))
        self.assertNotIn("CTR_DROP_REVIEW", review_flags(Metric("/x", 20, 1000, 8.5), old))

    def test_click_drop(self):
        old = Metric("/x", 60, 1000, 5.0)
        now = Metric("/x", 30, 1000, 12.0)
        self.assertIn("CLICK_DROP_REVIEW", review_flags(now, old))

    def test_missing_prior_does_not_become_zero(self):
        now = Metric("/x", 1, 200, 12.0)
        report = render_report({"/x": now}, {}, "page")
        self.assertIn("NOT_IN_PREVIOUS_EXPORT", report)
        self.assertIn("UNKNOWN", report)
        self.assertIn("NOT proof of zero impressions", report)

    def test_empty_report_uses_no_false_fixes(self):
        now = Metric("/x", 3, 30, 2.0)
        report = render_report({"/x": now}, {"/x": now}, "page")
        self.assertIn("No rows met", report)
        self.assertIn("review rows: 0", report)

    def test_markdown_escape(self):
        now = Metric("/x|y", 2, 200, 13)
        report = render_report({now.key: now}, {}, "query")
        self.assertIn("/x\\|y", report)


if __name__ == "__main__":
    unittest.main()
