import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from check_site import robots_result  # noqa: E402

class RobotsTests(unittest.TestCase):
    @patch("check_site.origin_for", return_value="https://example.com/")
    @patch("check_site.safe_fetch")
    def test_robots_503_has_high_severity_hint(self, fetch, origin):
        fetch.return_value = SimpleNamespace(error=None, status_code=503, body="", url="https://example.com/robots.txt")
        result, _ = robots_result("https://example.com/", 5)
        self.assertEqual(result["status"], "warn")
        self.assertEqual(result["severity_hint"], "high")
if __name__ == "__main__":
    unittest.main()
