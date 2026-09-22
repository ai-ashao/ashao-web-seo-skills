import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from site_audit import crawl_site, run_site_audit  # noqa: E402

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
    def test_crawl_prioritizes_internal_graph_before_sitemap_backlog(self, fetch):
        pages = {
            "https://example.com/": '<title>Home</title><h1>Home</h1><a href="/category">Category</a>',
            "https://example.com/category": '<title>Category</title><h1>Category</h1><a href="/font/a">A</a>',
            "https://example.com/font/a": '<title>A</title><h1>A</h1><link rel="canonical" href="/font/a">',
            "https://example.com/font/b": '<title>B</title><h1>B</h1><link rel="canonical" href="/font/b">',
            "https://example.com/font/c": '<title>C</title><h1>C</h1><link rel="canonical" href="/font/c">',
        }
        def side_effect(url, timeout):
            return SimpleNamespace(error=None, status_code=200, body=pages[url], url=url, headers={"Content-Type":"text/html"}, redirect_chain=[])
        fetch.side_effect = side_effect
        result = crawl_site(
            "https://example.com/",
            ["https://example.com/font/a", "https://example.com/font/b", "https://example.com/font/c"],
            "toolsite", max_pages=3, timeout=5,
        )
        checked = {page["requested_url"] for page in result["pages"]}
        self.assertEqual(checked, {"https://example.com/", "https://example.com/category", "https://example.com/font/a"})

    @patch("site_audit.safe_fetch")
    def test_query_state_canonicalization_is_not_a_p1_canonical_defect(self, fetch):
        pages = {
            "https://example.com/": '<title>Home</title><h1>Home</h1><link rel="canonical" href="/"><a href="/?focus=one">One</a><a href="/?focus=two">Two</a>',
            "https://example.com/?focus=one": '<title>Home</title><h1>Home</h1><link rel="canonical" href="/">',
            "https://example.com/?focus=two": '<title>Home</title><h1>Home</h1><link rel="canonical" href="/">',
        }
        def side_effect(url, timeout):
            return SimpleNamespace(error=None, status_code=200, body=pages[url], url=url, headers={"Content-Type":"text/html"}, redirect_chain=[])
        fetch.side_effect = side_effect
        result = run_site_audit("https://example.com/", [], "saas", max_pages=10, timeout=5)
        findings = result["analysis"]["findings"]
        codes = {item["code"] for item in findings}
        self.assertNotIn("NON_SELF_CANONICAL_PUBLIC", codes)
        self.assertNotIn("CANONICAL_COLLISION", codes)
        self.assertIn("INTERNAL_LINK_TO_CANONICALIZED_QUERY", codes)
        query_findings = [item for item in findings if item["code"] == "INTERNAL_LINK_TO_CANONICALIZED_QUERY"]
        self.assertEqual(len(query_findings), 1)
        query_finding = query_findings[0]
        self.assertEqual(query_finding["priority"], "P2")
        self.assertEqual(query_finding["evidence"]["unique_query_urls"], 2)

    @patch("site_audit.safe_fetch")
    def test_truncated_crawl_downgrades_orphan_to_candidate(self, fetch):
        pages = {
            "https://example.com/": '<title>Home</title><h1>Home</h1>',
            "https://example.com/orphan-a": '<title>A</title><h1>A</h1><link rel="canonical" href="/orphan-a">',
            "https://example.com/orphan-b": '<title>B</title><h1>B</h1><link rel="canonical" href="/orphan-b">',
            "https://example.com/orphan-c": '<title>C</title><h1>C</h1><link rel="canonical" href="/orphan-c">',
        }
        def side_effect(url, timeout):
            return SimpleNamespace(error=None, status_code=200, body=pages[url], url=url, headers={"Content-Type":"text/html"}, redirect_chain=[])
        fetch.side_effect = side_effect
        result = run_site_audit(
            "https://example.com/",
            ["https://example.com/orphan-a", "https://example.com/orphan-b", "https://example.com/orphan-c"],
            "toolsite", max_pages=3, timeout=5,
        )
        findings = result["analysis"]["findings"]
        self.assertNotIn("ORPHAN_SITEMAP_PAGE", {item["code"] for item in findings})
        candidates = [item for item in findings if item["code"] == "ORPHAN_SITEMAP_CANDIDATE"]
        self.assertEqual(len(candidates), 1)
        candidate = candidates[0]
        self.assertEqual(candidate["priority"], "P2")
        self.assertEqual(candidate["evidence"]["candidate_count"], 2)
        self.assertGreater(candidate["evidence"]["queue_remaining"], 0)

    @patch("site_audit.safe_fetch")
    def test_trailing_slash_variant_does_not_create_canonical_collision(self, fetch):
        pages = {
            "https://example.com/": '<title>Home</title><h1>Home</h1><link rel="canonical" href="/">',
            "https://example.com": '<title>Home</title><h1>Home</h1><link rel="canonical" href="/">',
        }
        def side_effect(url, timeout):
            return SimpleNamespace(error=None, status_code=200, body=pages[url], url=url, headers={"Content-Type":"text/html"}, redirect_chain=[])
        fetch.side_effect = side_effect
        result = run_site_audit("https://example.com/", ["https://example.com"], "saas", max_pages=10, timeout=5)
        codes = {item["code"] for item in result["analysis"]["findings"]}
        self.assertNotIn("CANONICAL_COLLISION", codes)
        self.assertNotIn("DUPLICATE_TITLE", codes)
        self.assertNotIn("DUPLICATE_H1", codes)
        self.assertNotIn("DUPLICATE_META_DESCRIPTION", codes)

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
