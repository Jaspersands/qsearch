import json
import tempfile
import unittest
from pathlib import Path

from tools.check_site import hardcoded_metrics, main, missing_references


class CheckSiteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "research").mkdir()
        (self.root / "research" / "progress_snapshot.json").write_text(
            json.dumps({"metrics": {"experiments": 796, "negative_results": 1326, "proof_debts": 24}})
        )
        (self.root / "tests").mkdir()
        (self.root / "tests" / "test_real.py").write_text("")
        (self.root / "other.html").write_text("<p>ok</p>")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_page(self, html: str) -> None:
        (self.root / "index.html").write_text(html)

    def test_existing_references_and_links_pass(self) -> None:
        self.write_page(
            '<code>tests/test_real.py</code> '
            '<a href="https://github.com/x/blob/main/research/progress_snapshot.json">s</a> '
            '<a href="other.html#top">o</a> <a href="https://example.com/page.html">e</a>'
        )
        self.assertEqual(missing_references(self.root), [])

    def test_missing_reference_is_reported(self) -> None:
        self.write_page('<a href="https://github.com/x/blob/main/tests/test_gone.py">t</a>')
        self.assertEqual(
            missing_references(self.root), ["index.html: references missing file tests/test_gone.py"]
        )

    def test_broken_internal_link_is_reported(self) -> None:
        self.write_page('<a href="missing.html">m</a>')
        self.assertEqual(missing_references(self.root), ["index.html: links to missing page missing.html"])

    def test_js_files_are_scanned(self) -> None:
        self.write_page("<p></p>")
        (self.root / "site" / "js").mkdir(parents=True)
        (self.root / "site" / "js" / "page.js").write_text('const DATA = "site/data/gone.json";')
        self.assertEqual(
            missing_references(self.root), ["site/js/page.js: references missing file site/data/gone.json"]
        )

    def test_hardcoded_metric_values_are_reported(self) -> None:
        self.write_page("<p>796 experiments, 1,326 negatives, 24 debts, 2026-07-96, 17960</p>")
        self.assertEqual(
            hardcoded_metrics(self.root),
            [
                "index.html: hardcodes the current metric value 796",
                "index.html: hardcodes the current metric value 1,326",
            ],
        )

    def test_main_returns_nonzero_on_problems(self) -> None:
        self.write_page('<a href="missing.html">m</a>')
        self.assertEqual(main(["--root", str(self.root)]), 1)
        self.write_page("<p>fine</p>")
        self.assertEqual(main(["--root", str(self.root)]), 0)


if __name__ == "__main__":
    unittest.main()
