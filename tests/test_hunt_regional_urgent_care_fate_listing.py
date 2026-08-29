import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_LAYERS = (ROOT / "index.html", ROOT / "listings.html")
OFFICIAL_URL = "https://urgentcare.huntregional.org/location/hunt-regional-urgent-care-fate/"
EXPECTED_RECORD = (
    "<div class='biz-card'><strong><a href='"
    + OFFICIAL_URL
    + "' target='_blank' rel='noopener'>Hunt Regional Urgent Care Fate</a></strong>"
    "<span>5000 E IH-30, Suite 120, Fate, TX 75189</span></div>"
)


class HuntRegionalUrgentCareFateListingContract(unittest.TestCase):
    def test_official_listing_is_consistent_and_unique_in_public_layers(self):
        for path in PUBLIC_LAYERS:
            html = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                # Count only in non-script content to avoid JSON-LD collisions
                visible_html = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
                self.assertEqual(visible_html.count("Hunt Regional Urgent Care Fate"), 1)
                self.assertEqual(visible_html.count(OFFICIAL_URL), 1)
                self.assertIn(EXPECTED_RECORD, html)

    def test_listing_has_no_invented_rating_or_review_claim(self):
        for path in PUBLIC_LAYERS:
            html = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                cards = re.findall(r"<div class='biz-card'>.*?</div>", html)
                matching = [card for card in cards if "Hunt Regional Urgent Care Fate" in card]
                self.assertEqual(len(matching), 1)
                self.assertNotIn("stars", matching[0].lower())
                self.assertNotIn("review", matching[0].lower())
                self.assertEqual(matching[0].count("<span>"), 1)

    def test_indexing_control_files_remain_present(self):
        self.assertTrue((ROOT / "robots.txt").is_file())
        self.assertTrue((ROOT / "sitemap.xml").is_file())


if __name__ == "__main__":
    unittest.main()
