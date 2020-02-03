from unittest import TestCase

from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import League


class TestSearch(TestCase):
    def test_search_ja(self):
        results = client.search(term="ja")
        self.assertIsNotNone(results["players"])

    def test_search_jaebaebae(self):
        results = client.search(term="jaebaebae")
        self.assertListEqual([], results["players"])

    def test_length_of_kobe_search_results(self):
        results = client.search(term="kobe")
        self.assertEqual(4, len(results["players"]))

    def test_players_in_kobe_search_results(self):
        results = client.search(term="kobe")
        self.assertListEqual(
            [
                {
                    "name": "Kobe Bryant",
                    "identifier": "bryanko01",
                    "leagues": {League.NATIONAL_BASKETBALL_ASSOCIATION}
                },
                {
                    "name": "Ruben Patterson",
                    "identifier": "patteru01",
                    "leagues": {League.NATIONAL_BASKETBALL_ASSOCIATION}
                },
                {
                    "name": "Dion Waiters",
                    "identifier": "waitedi01",
                    "leagues": {League.NATIONAL_BASKETBALL_ASSOCIATION}
                },
                {
                    "name": "Oleksandr Kobets",
                    "identifier": "kobetol01",
                    "leagues": set()
                }
            ],
            results["players"]
        )

    def test_exact_search_result(self):
        results = client.search(term="kobe bryant")
        self.assertEqual(
            [
                {
                    "name": "Kobe Bryant",
                    "identifier": "bryanko01",
                    "leagues": {League.NATIONAL_BASKETBALL_ASSOCIATION}
                }
            ],
            results["players"]
        )
