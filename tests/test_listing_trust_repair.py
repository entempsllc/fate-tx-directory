import unittest
import os
import re

class TestListingTrustRepair(unittest.TestCase):
    def setUp(self):
        self.root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.index_path = os.path.join(self.root, 'index.html')
        self.listings_path = os.path.join(self.root, 'listings.html')

    def test_no_unverified_stars_in_index(self):
        with open(self.index_path, 'r') as f:
            content = f.read()
        
        # Matches "4.4 stars", "4 stars", " stars", etc. inside spans or just as text
        # Specifically targeting the pattern found in the biz-cards
        matches = re.findall(r'<span>\d?\.?\d?\s*stars?</span>', content, re.IGNORECASE)
        self.assertEqual(len(matches), 0, f"Found unverified stars in index.html: {matches}")

    def test_no_unverified_stars_in_listings(self):
        with open(self.listings_path, 'r') as f:
            content = f.read()
        
        matches = re.findall(r'<span>\d?\.?\d?\s*stars?</span>', content, re.IGNORECASE)
        self.assertEqual(len(matches), 0, f"Found unverified stars in listings.html: {matches}")

    def test_no_malformed_body_in_index(self):
        with open(self.index_path, 'r') as f:
            content = f.read()
        
        # Check if </body> appears more than once or before the end
        body_count = content.count('</body>')
        self.assertEqual(body_count, 1, f"Found {body_count} </body> tags in index.html")

if __name__ == '__main__':
    unittest.main()
