import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from release_residue import analyze_release_residue  # noqa: E402


class ReleaseResidueTests(unittest.TestCase):
    def test_detects_deterministic_release_blockers(self):
        html = """
        <title>Tool</title>
        <h1>Useful Tool</h1>
        <button>TODO: connect production API</button>
        <p>Request failed: API key not configured.</p>
        <a href="/">Try http://localhost:3000 instead</a>
        """
        result = analyze_release_residue(html, "https://example.com/tool", "PUBLIC_TOOL")
        codes = {item["code"] for item in result["findings"]}
        self.assertEqual(result["status"], "fail")
        self.assertIn("TODO_MARKER", codes)
        self.assertIn("MISSING_RUNTIME_CONFIG", codes)
        self.assertIn("LOCAL_DEVELOPMENT_ENDPOINT", codes)
        self.assertGreaterEqual(result["summary"]["P0"], 3)

    def test_detects_mvp_and_phase_language_on_marketing_page(self):
        html = "<h1>Image Tool</h1><p>Our MVP covers uploads now. Batch mode arrives in Phase 2.</p>"
        result = analyze_release_residue(html, "https://example.com/", "MARKETING")
        by_code = {item["code"]: item for item in result["findings"]}
        self.assertEqual(by_code["MVP_LANGUAGE"]["severity"], "P1")
        self.assertEqual(by_code["PHASE_LANGUAGE"]["severity"], "P1")
        self.assertEqual(result["status"], "review")

    def test_downgrades_dev_process_language_for_docs(self):
        html = "<h1>API Docs</h1><p>The MVP used a different endpoint during Phase 1.</p>"
        result = analyze_release_residue(html, "https://example.com/docs/api", "DOCS")
        by_code = {item["code"]: item for item in result["findings"]}
        self.assertEqual(by_code["MVP_LANGUAGE"]["severity"], "P2")
        self.assertEqual(by_code["PHASE_LANGUAGE"]["severity"], "P2")

    def test_suppresses_contextual_infrastructure_jargon_for_docs(self):
        html = "<h1>Storage API</h1><p>Objects are stored in Cloudflare R2 and delivered with a presigned URL.</p>"
        result = analyze_release_residue(html, "https://example.com/docs/storage", "DOCS")
        codes = {item["code"] for item in result["findings"]}
        self.assertNotIn("INFRASTRUCTURE_JARGON", codes)
        self.assertNotIn("PRESIGNED_URL_JARGON", codes)

    def test_flags_infrastructure_jargon_for_general_marketing_copy(self):
        html = "<h1>Download faster</h1><p>Your file is fetched from our R2 bucket using a presigned URL.</p>"
        result = analyze_release_residue(html, "https://example.com/download", "SEO_LANDING")
        by_code = {item["code"]: item for item in result["findings"]}
        self.assertEqual(by_code["INFRASTRUCTURE_JARGON"]["severity"], "P2")
        self.assertEqual(by_code["PRESIGNED_URL_JARGON"]["severity"], "P2")

    def test_scans_control_attributes_and_alerts(self):
        html = '<input placeholder="localhost:8787"><div role="alert">TypeError: failed to process payload</div>'
        result = analyze_release_residue(html, "https://example.com/tool", "PUBLIC_TOOL")
        elements = {item["element"] for item in result["findings"]}
        self.assertIn("input[placeholder]", elements)
        self.assertIn("div[role=alert]", elements)

    def test_ignores_code_and_preformatted_examples(self):
        html = """
        <h1>Developer article</h1>
        <pre>TODO localhost:3000 TypeError: example</pre>
        <code>Cloudflare R2 bucket</code>
        <p>Production copy is clean.</p>
        """
        result = analyze_release_residue(html, "https://example.com/guides/debugging", "CONTENT")
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["status"], "info")

    def test_body_fallback_catches_unwrapped_copy(self):
        html = "<main><div>This feature is not yet implemented.</div></main>"
        result = analyze_release_residue(html, "https://example.com/tool", "PUBLIC_TOOL")
        finding = next(item for item in result["findings"] if item["code"] == "NOT_IMPLEMENTED_LANGUAGE")
        self.assertEqual(finding["element"], "visible_body")


if __name__ == "__main__":
    unittest.main()
