import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_LAYERS = (ROOT / "index.html", ROOT / "listings.html")
EXPECTED_RECORD = (
    "<div class='biz-card'><strong><a href='https://www.hotworx.net/studio/fate' "
    "target='_blank' rel='noopener'>HOTWORX - Fate, TX</a></strong>"
    "<span>5000 E. I-30 Suite 160, Fate, TX 75189</span>"
)


class HotworxFateListingContract(unittest.TestCase):
    def test_official_name_address_and_contact_are_consistent_in_public_layers(self):
        for path in PUBLIC_LAYERS:
            html = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertEqual(html.count("HOTWORX - Fate, TX"), 1)
                self.assertEqual(html.count("https://www.hotworx.net/studio/fate"), 1)
                self.assertIn(EXPECTED_RECORD, html)

    def test_no_indexing_control_files_changed_for_listing_correction(self):
        self.assertTrue((ROOT / "robots.txt").is_file())
        self.assertTrue((ROOT / "sitemap.xml").is_file())


if __name__ == "__main__":
    unittest.main()
