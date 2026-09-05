import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from check_page import analyze_html, hreflang_code_supported_format, validate_canonical_target  # noqa: E402

class PageCheckTests(unittest.TestCase):
    def test_multiple_robots_meta_are_aggregated(self):
        html = '<meta name="robots" content="noindex"><meta name="robots" content="follow"><h1>Tool</h1>'
        check = analyze_html(html, "https://example.com/tool", None, True)["indexability_directives"]
        self.assertEqual(check["status"], "fail")
        self.assertIn("noindex", check["directives"])
        self.assertIn("follow", check["directives"])
        self.assertEqual(len(check["meta_robots"]), 2)

    def test_conflicting_canonical_is_detected(self):
        html = '<link rel="canonical" href="/a"><link rel="canonical" href="/b"><h1>Tool</h1>'
        check = analyze_html(html, "https://example.com/tool", None, True)["canonical"]
        self.assertTrue(check["conflicting"])
        self.assertEqual(check["status"], "fail")

    def test_identical_duplicate_canonical_is_review_only(self):
        html = '<link rel="canonical" href="/tool"><link rel="canonical" href="https://example.com/tool"><h1>Tool</h1>'
        check = analyze_html(html, "https://example.com/tool", None, True)["canonical"]
        self.assertFalse(check["conflicting"])
        self.assertTrue(check["duplicate_identical_tags"])
        self.assertEqual(check["status"], "review")

    def test_hreflang_rejects_three_letter_and_numeric_region(self):
        self.assertFalse(hreflang_code_supported_format("eng"))
        self.assertFalse(hreflang_code_supported_format("en-123"))
        self.assertFalse(hreflang_code_supported_format("es-419"))
        self.assertTrue(hreflang_code_supported_format("zh-Hant-TW"))
        self.assertTrue(hreflang_code_supported_format("en-US"))
        self.assertTrue(hreflang_code_supported_format("x-default"))

    def test_scripts_never_claim_rendered_parity(self):
        html = '<title>Tool</title><h1>Tool</h1><p>Lots of static content here.</p><script src="/app.js"></script>'
        check = analyze_html(html, "https://example.com/tool", None, True)["rendering"]
        self.assertEqual(check["status"], "unassessed")

    def test_private_route_without_noindex_is_warned(self):
        check = analyze_html("<title>Dashboard</title><h1>Dashboard</h1>", "https://example.com/dashboard", None, False)["indexability_directives"]
        self.assertEqual(check["status"], "warn")

    @patch("check_page.safe_fetch")
    def test_canonical_target_validation_fails_noindex_target(self, fetch):
        fetch.return_value = SimpleNamespace(
            error=None, status_code=200, body='<meta name="robots" content="noindex"><title>Old</title><h1>Old</h1>',
            url="https://example.com/canonical", headers={"Content-Type": "text/html"}, redirect_chain=[]
        )
        check = {"value": "https://example.com/canonical", "conflicting": False}
        result = validate_canonical_target(check, True, 5)
        self.assertEqual(result["status"], "fail")
        self.assertTrue(result["noindex"])

if __name__ == "__main__":
    unittest.main()
