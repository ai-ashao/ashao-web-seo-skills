import sys
import unittest
from pathlib import Path
SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from profiles import classify_route, decide_route, detect_profile  # noqa: E402

class ProfileTests(unittest.TestCase):
    def test_hybrid_routes_get_page_level_expectations(self):
        self.assertTrue(decide_route("https://x.test/tools/pdf", "hybrid").expected_indexable)
        self.assertTrue(decide_route("https://x.test/pricing", "hybrid").expected_indexable)
        self.assertFalse(decide_route("https://x.test/dashboard", "hybrid").expected_indexable)
        self.assertFalse(decide_route("https://x.test/billing", "hybrid").expected_indexable)

    def test_unknown_route_stays_unassessed(self):
        self.assertIsNone(decide_route("https://x.test/legal", "hybrid").expected_indexable)

    def test_auto_detection_recognizes_hybrid(self):
        result = detect_profile(["https://x.test/tools/pdf", "https://x.test/pricing", "https://x.test/dashboard"])
        self.assertEqual(result["profile"], "hybrid")

    def test_root_class_depends_on_profile(self):
        self.assertEqual(classify_route("https://x.test/", "toolsite"), "PUBLIC_TOOL")
        self.assertEqual(classify_route("https://x.test/", "saas"), "MARKETING")

if __name__ == "__main__":
    unittest.main()
