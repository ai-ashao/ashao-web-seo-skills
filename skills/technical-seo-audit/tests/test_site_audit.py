import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from site_audit import run_site_audit  # noqa: E402

PAGES = {
    "https://example.com/": '<title>Home</title><h1>Home</h1><a href="/tools/pdf">PDF</a><a href="/dashboard">Dashboard</a>',
    "https://example.com/tools/pdf": '<title>PDF Tool</title><h1>PDF Tool</h1><link rel="canonical" href="/tools/pdf">',
    "https://example.com/dashboard": '<title>Dashboard</title><h1>Dashboard</h1>',
    "https://example.com/orphan": '<title>Orphan</title><h1>Orphan</h1><link rel="canonical" href="/orphan">',
    "https://example.com/noindex": '<meta name="robots" content="noindex"><title>Noindex</title><h1>Noindex</h1><link rel="canonical" href="/noindex">',
}

class SiteAuditTests(unittest.TestCase):
    @patch("site_audit.safe_fetch")
    def test_hybrid_site_finds_private_leak_orphan_and_sitemap_noindex(self, fetch):
        def side_effect(url, timeout):
            body = PAGES.get(url)
            if body is None:
                return SimpleNamespace(error=None, status_code=404, body="", url=url, headers={"Content-Type":"text/html"}, redirect_chain=[])
            return SimpleNamespace(error=None, status_code=200, body=body, url=url, headers={"Content-Type":"text/html"}, redirect_chain=[])
        fetch.side_effect = side_effect
        result = run_site_audit(
            "https://example.com/",
            ["https://example.com/tools/pdf", "https://example.com/orphan", "https://example.com/noindex"],
            "hybrid", max_pages=20, timeout=5,
        )
        codes = {f["code"] for f in result["analysis"]["findings"]}
        self.assertIn("PRIVATE_ROUTE_INDEXABLE", codes)
        self.assertIn("ORPHAN_SITEMAP_PAGE", codes)
        self.assertIn("SITEMAP_NOINDEX", codes)

    @patch("site_audit.safe_fetch")
    def test_auto_profile_detects_hybrid_after_crawl(self, fetch):
        pages = dict(PAGES)
        pages["https://example.com/"] = '<title>Home</title><h1>Home</h1><a href="/tools/pdf">PDF</a><a href="/pricing">Pricing</a><a href="/dashboard">Dashboard</a>'
        pages["https://example.com/pricing"] = '<title>Pricing</title><h1>Pricing</h1>'
        def side_effect(url, timeout):
            body = pages.get(url, '<title>X</title><h1>X</h1>')
            return SimpleNamespace(error=None, status_code=200, body=body, url=url, headers={"Content-Type":"text/html"}, redirect_chain=[])
        fetch.side_effect = side_effect
        result = run_site_audit("https://example.com/", [], "auto", max_pages=20, timeout=5)
        self.assertEqual(result["effective_profile"], "hybrid")

    @patch("site_audit.safe_fetch")
    def test_duplicate_meta_descriptions_are_reported_as_findings(self, fetch):
        pages = {
            "https://example.com/": (
                '<title>Home</title><meta name="description" content="Shared">'
                '<h1>Home</h1><a href="/pricing">Pricing</a>'
            ),
            "https://example.com/pricing": (
                '<title>Pricing</title><meta name="description" content="Shared">'
                '<h1>Pricing</h1>'
            ),
        }

        def side_effect(url, timeout):
            return SimpleNamespace(
                error=None,
                status_code=200,
                body=pages[url],
                url=url,
                headers={"Content-Type": "text/html"},
                redirect_chain=[],
            )

        fetch.side_effect = side_effect
        result = run_site_audit("https://example.com/", [], "saas", max_pages=20, timeout=5)
        findings = result["analysis"]["findings"]
        duplicate = next(item for item in findings if item["code"] == "DUPLICATE_META_DESCRIPTION")
        self.assertEqual(duplicate["priority"], "P2")
        self.assertEqual(
            duplicate["evidence"]["urls"],
            ["https://example.com/", "https://example.com/pricing"],
        )

    @patch("site_audit.safe_fetch")
    def test_public_copy_release_residue_becomes_site_finding(self, fetch):
        pages = {
            "https://example.com/": (
                '<title>Home</title><h1>Home</h1>'
                '<p>This MVP ships in Phase 1 while we finish the implementation.</p>'
            ),
        }

        def side_effect(url, timeout):
            return SimpleNamespace(
                error=None,
                status_code=200,
                body=pages[url],
                url=url,
                headers={"Content-Type": "text/html"},
                redirect_chain=[],
            )

        fetch.side_effect = side_effect
        result = run_site_audit("https://example.com/", [], "saas", max_pages=10, timeout=5)
        findings = result["analysis"]["findings"]
        codes = {item["code"] for item in findings}
        self.assertIn("PUBLIC_COPY_MVP_LANGUAGE", codes)
        self.assertIn("PUBLIC_COPY_PHASE_LANGUAGE", codes)
        mvp = next(item for item in findings if item["code"] == "PUBLIC_COPY_MVP_LANGUAGE")
        self.assertEqual(mvp["priority"], "P1")
        self.assertEqual(mvp["evidence"]["element"], "p")


if __name__ == "__main__":
    unittest.main()
