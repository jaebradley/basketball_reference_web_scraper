import json
import os
from unittest import TestCase

import requests_mock

from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import League, OutputType, OutputWriteOption


@requests_mock.Mocker()
class TestJa(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/ja/0.html"
        ), 'r') as file_input: self._html = file_input.read()
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/ja/1.html"
        ), 'r') as file_input: self._1_html = file_input.read()
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/ja/2.html"
        ), 'r') as file_input: self._2_html = file_input.read()
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/ja/3.html"
        ), 'r') as file_input: self._3_html = file_input.read()
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/ja/4.html"
        ), 'r') as file_input: self._4_html = file_input.read()
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/ja/5.html"
        ), 'r') as file_input: self._5_html = file_input.read()
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/ja/6.html"
        ), 'r') as file_input: self._6_html = file_input.read()
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/ja/7.html"
        ), 'r') as file_input: self._7_html = file_input.read()
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/ja/8.html"
        ), 'r') as file_input: self._8_html = file_input.read()

    def test_length(self, m):
        m.get("https://www.basketball-reference.com/search/search.fcgi?search=ja",
              text=self._html,
              status_code=200)
        m.get("https://www.basketball-reference.com/search/search.fcgi?search=ja&i=players&offset=100",
              text=self._1_html,
              status_code=200)
        m.get("https://www.basketball-reference.com/search/search.fcgi?search=ja&i=players&offset=200",
              text=self._2_html,
              status_code=200)
        m.get("https://www.basketball-reference.com/search/search.fcgi?search=ja&i=players&offset=300",
              text=self._3_html,
              status_code=200)
        m.get("https://www.basketball-reference.com/search/search.fcgi?search=ja&i=players&offset=400",
              text=self._4_html,
              status_code=200)
        m.get("https://www.basketball-reference.com/search/search.fcgi?search=ja&i=players&offset=500",
              text=self._5_html,
              status_code=200)
        m.get("https://www.basketball-reference.com/search/search.fcgi?search=ja&i=players&offset=600",
              text=self._6_html,
              status_code=200)
        m.get("https://www.basketball-reference.com/search/search.fcgi?search=ja&i=players&offset=700",
              text=self._7_html,
              status_code=200)
        m.get("https://www.basketball-reference.com/search/search.fcgi?search=ja&i=players&offset=800",
              text=self._8_html,
              status_code=200)
        results = client.search(term="ja")
        self.assertEqual(863, len(results["players"]))
        self.assertEqual({
                    "name": "LeBron James",
                    "identifier": "jamesle01",
                    "leagues": set()
                }, results["players"][0])

@requests_mock.Mocker()
class TestAlonzoMourning(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/Alonzo Mourning.html"
        ), 'r') as file_input: self._html = file_input.read()

    def test_result(self, m):
        m.get(f"https://www.basketball-reference.com/search/search.fcgi?search=Alonzo+Mourning",
              text=self._html,
              status_code=200)
        results = client.search(term="Alonzo Mourning")
        self.assertEqual(
            [
                {
                    "name": "Alonzo Mourning",
                    "identifier": "mournal01",
                    # Basketball-Reference moved leagues from the search results
                    "leagues": set()
                }
            ],
            results["players"]
        )


class TestSearchInMemory(TestCase):
    def test_search_ja(self):
        results = client.search(term="ja")
        self.assertLessEqual(498, len(results["players"]))

    def test_search_alonzo_mourning(self):
        results = client.search(term="Alonzo Mourning")
        self.assertEqual(
            [
                {
                    "name": "Alonzo Mourning",
                    "identifier": "mournal01",
                    "leagues": {League.NATIONAL_BASKETBALL_ASSOCIATION}
                }
            ],
            results["players"]
        )

    def test_search_alonz(self):
        results = client.search(term="Alonz")
        self.assertGreaterEqual(6, len(results["players"]))

    def test_search_dominique_wilkins(self):
        results = client.search(term="Dominique Wilkins")
        self.assertEqual(
            [
                {
                    "name": "Dominique Wilkins",
                    "identifier": "wilkido01",
                    "leagues": {League.NATIONAL_BASKETBALL_ASSOCIATION}
                }
            ],
            results["players"]
        )

    def test_search_rick_barry(self):
        results = client.search(term="Rick Barry")
        self.assertEqual(
            [
                {
                    "name": "Rick Barry",
                    "identifier": "barryri01",
                    "leagues": {League.NATIONAL_BASKETBALL_ASSOCIATION, League.AMERICAN_BASKETBALL_ASSOCIATION}
                }
            ],
            results["players"]
        )

    def test_search_jaebaebae(self):
        results = client.search(term="jaebaebae")
        self.assertListEqual([], results["players"])

    def test_search_results_key(self):
        results = client.search(term="jaebaebae")
        self.assertListEqual(list(results), ["players"])

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


class TestSearchJSONOutput(TestCase):
    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/ko_search.json",
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/ko_search.json",
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def test_ko_search_json_output_includes_expected_json_output(self):
        client.search(
            term="ko",
            output_type=OutputType.JSON,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )
        with open(self.output_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            output_data = json.load(output_file)
            expected_output_data = json.load(expected_output_file)
            for expected_data_row in expected_output_data:
                self.assertTrue(expected_data_row in output_data)


class TestSearchCSVOutput(TestCase):
    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/ko_search.csv",
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/ko_search.csv",
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def test_ko_csv_output_search_includes_expected_csv_output(self):
        client.search(
            term="ko",
            output_type=OutputType.CSV,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )

        with open(self.output_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            output_data = output_file.readlines()
            expected_output_data = expected_output_file.readlines()
            for expected_data_row in expected_output_data:
                # TODO: @jaebradley this is freakin' gross but sets are not ordered (duh)
                # so serialization of the set of leagues will not be consistent.
                # Need to find a way to use an ordered set or something for this.
                # In the interim, ignore serialized sets of leagues - quick and dirty way
                # is to look for `-` (this ignores players with a `-` but I'll take the tradeoff for now)
                if "-" not in expected_data_row:
                    self.assertTrue(expected_data_row in output_data)
