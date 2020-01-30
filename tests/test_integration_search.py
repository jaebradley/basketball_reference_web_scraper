from unittest import TestCase

from basketball_reference_web_scraper import client


class TestSearch(TestCase):
    def test_search_ja(self):
        results = client.search(term="ja")
        self.assertIsNotNone(results)
