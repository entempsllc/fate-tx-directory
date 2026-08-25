import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")


class OfficialCityServiceLinksContract(unittest.TestCase):
    def test_city_services_use_current_official_fate_destinations(self):
        city_section = re.search(
            r'<!-- CITY SERVICES -->(.*?)<!-- EVENTS -->', INDEX, re.DOTALL
        )
        if city_section is None:
            self.fail("City services section is missing")
        html = city_section.group(1)

        expected = {
            "https://www.fatetx.gov/": "Official city homepage",
            "https://www.fatetx.gov/561/Trash-Services": "Official trash services",
            "https://www.fatetx.gov/152/Applications-Fee-Info": "Official permit applications and fees",
            "https://www.fatetx.gov/153/Planning-Development": "Official planning and development",
        }
        for url, label in expected.items():
            with self.subTest(url=url):
                self.assertIn(f'href="{url}"', html)
                self.assertIn(label, html)

        self.assertNotIn("cityoffate.com", html.lower())

    def test_indexing_metadata_remains_unchanged(self):
        self.assertEqual(
            re.findall(r'<link rel="canonical" href="([^"]+)">', INDEX),
            ["https://fatetxdirectory.com/"],
        )
        self.assertNotRegex(INDEX.lower(), r'<meta[^>]+name="robots"')


if __name__ == "__main__":
    unittest.main()
