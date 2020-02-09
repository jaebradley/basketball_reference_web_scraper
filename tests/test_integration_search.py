from unittest import TestCase

from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import League, OutputType, OutputWriteOption


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

    def test_large_search_pagination(self):
        results = client.search(term="a")
        self.assertGreaterEqual(len(results["players"]), 960)

    def test_output_to_json(self):
        client.search(
            term="ko",
            output_type=OutputType.JSON,
            output_file_path="./ko-search.json",
            output_write_option=OutputWriteOption.WRITE,
        )

    def test_output_to_csv(self):
        client.search(
            term="ko",
            output_type=OutputType.CSV,
            output_file_path="./ko-search.csv",
            output_write_option=OutputWriteOption.WRITE,
        )
