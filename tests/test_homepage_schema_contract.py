import unittest
import os
import json
from bs4 import BeautifulSoup

class TestHomepageSchemaContract(unittest.TestCase):
    def setUp(self):
        self.index_path = "/tmp/fate-seo-20260829/index.html"
        with open(self.index_path, 'r') as f:
            self.soup = BeautifulSoup(f.read(), 'html.parser')

    def test_json_ld_present(self):
        scripts = self.soup.find_all('script', type='application/ld+json')
        self.assertGreater(len(scripts), 0, "JSON-LD script missing from homepage")
        
        found_schema = False
        for script in scripts:
            if not script.string: continue
            try:
                data = json.loads(script.string)
                if data.get('@type') in ['ItemList', 'LocalBusiness']:
                    found_schema = True
                    # Verify at least one business is in the list
                    if data.get('@type') == 'ItemList':
                        items = data.get('itemListElement', [])
                        self.assertGreater(len(items), 0, "ItemList is empty")
                        self.assertEqual(items[0].get('item', {}).get('name'), "Hunt Regional Urgent Care Fate")
                    break
            except Exception as e:
                print(f"Error parsing JSON-LD: {e}")
                continue
        self.assertTrue(found_schema, "No ItemList or LocalBusiness schema found in JSON-LD")

    def test_sitemap_includes_listings(self):
        sitemap_path = "/tmp/fate-seo-20260829/sitemap.xml"
        with open(sitemap_path, 'r') as f:
            content = f.read()
        self.assertIn("https://fatetxdirectory.com/listings.html", content, "/listings.html missing from sitemap.xml")

if __name__ == '__main__':
    unittest.main()
