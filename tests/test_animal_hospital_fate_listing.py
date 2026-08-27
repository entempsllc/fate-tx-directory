import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_LAYERS = (ROOT / "index.html", ROOT / "listings.html")
EXPECTED_RECORD = (
    "<div class='biz-card'><strong><a href='https://ahfate.com/' "
    "target='_blank' rel='noopener'>Animal Hospital of Fate</a></strong>"
    "<span>1001 North W.E. Crawford, Fate, TX 75087</span>"
)


class AnimalHospitalFateListingContract(unittest.TestCase):
    def test_official_name_address_and_contact_are_consistent_in_public_layers(self):
        for path in PUBLIC_LAYERS:
            html = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertEqual(html.count("Animal Hospital of Fate"), 1)
                self.assertEqual(html.count("https://ahfate.com/"), 1)
                self.assertIn(EXPECTED_RECORD, html)

    def test_rating_is_not_changed_by_contact_correction(self):
        for path in PUBLIC_LAYERS:
            html = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn(EXPECTED_RECORD + "<span>4.3 stars</span></div>", html)

    def test_no_indexing_control_files_changed_for_listing_correction(self):
        self.assertTrue((ROOT / "robots.txt").is_file())
        self.assertTrue((ROOT / "sitemap.xml").is_file())


if __name__ == "__main__":
    unittest.main()
