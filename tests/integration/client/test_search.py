import filecmp
import json
import os
from unittest import TestCase

import requests_mock

from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType, OutputWriteOption


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


@requests_mock.Mocker()
class TestDominiqueWilkins(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/Dominique Wilkins.html"
        ), 'r') as file_input: self._html = file_input.read()

    def test_result(self, m):
        m.get(f"https://www.basketball-reference.com/search/search.fcgi?search=Dominique+Wilkins",
              text=self._html,
              status_code=200)
        results = client.search(term="Dominique Wilkins")
        self.assertEqual(
            [
                {
                    "name": "Dominique Wilkins",
                    "identifier": "wilkido01",
                    "leagues": set()
                }
            ],
            results["players"]
        )


@requests_mock.Mocker()
class TestRickBarry(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/Rick Barry.html"
        ), 'r') as file_input: self._html = file_input.read()

    def test_result(self, m):
        m.get(f"https://www.basketball-reference.com/search/search.fcgi?search=Rick+Barry",
              text=self._html,
              status_code=200)
        results = client.search(term="Rick Barry")
        self.assertEqual(
            [
                {
                    "name": "Rick Barry",
                    "identifier": "barryri01",
                    "leagues": set()
                }
            ],
            results["players"]
        )


@requests_mock.Mocker()
class TestJaebaebae(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/jaebaebae.html"
        ), 'r') as file_input: self._html = file_input.read()

    def test_result(self, m):
        m.get(f"https://www.basketball-reference.com/search/search.fcgi?search=jaebaebae",
              text=self._html,
              status_code=200)
        results = client.search(term="jaebaebae")
        self.assertEqual(
            [],
            results["players"]
        )


@requests_mock.Mocker()
class TestKobeBryant(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/kobe bryant.html"
        ), 'r') as file_input: self._html = file_input.read()

    def test_result(self, m):
        m.get(f"https://www.basketball-reference.com/search/search.fcgi?search=kobe+bryant",
              text=self._html,
              status_code=200)
        results = client.search(term="kobe bryant")
        self.assertEqual(
            [
                {
                    "name": "Kobe Bryant",
                    "identifier": "bryanko01",
                    "leagues": set()
                }
            ],
            results["players"]
        )


@requests_mock.Mocker()
class TestKobe(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/kobe.html"
        ), 'r') as file_input: self._html = file_input.read()

    def test_result(self, m):
        m.get(f"https://www.basketball-reference.com/search/search.fcgi?search=kobe",
              text=self._html,
              status_code=200)
        results = client.search(term="kobe")
        self.assertEqual(
            [
                {
                    "name": "Kobe Bryant",
                    "identifier": "bryanko01",
                    "leagues": set()
                },
                {
                    "name": "Ruben Patterson",
                    "identifier": "patteru01",
                    "leagues": set()
                },
                {
                    "name": "Dion Waiters",
                    "identifier": "waitedi01",
                    "leagues": set()
                },
                {
                    "name": "Austin Reaves",
                    "identifier": "reaveau01",
                    "leagues": set()
                },
                {
                    "name": "Kobe Bufkin",
                    "identifier": "bufkiko01",
                    "leagues": set()
                },
                {
                    "name": "Kobe Brown",
                    "identifier": "brownko01",
                    "leagues": set()
                },
                {
                    "name": "Oleksandr Kobets",
                    "identifier": "kobetol01",
                    "leagues": set()
                }
            ],
            results["players"]
        )


@requests_mock.Mocker()
class TestSearchJSONFileOutput(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/kobe.html"
        ), 'r') as file_input: self._html = file_input.read()
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/search/kobe.json",
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/search/kobe.json",
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def test_file_output(self, m):
        m.get(f"https://www.basketball-reference.com/search/search.fcgi?search=kobe",
              text=self._html,
              status_code=200)

        client.search(
            term="kobe",
            output_type=OutputType.JSON,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )
        self.assertTrue(
            filecmp.cmp(
                self.output_file_path,
                self.expected_output_file_path))


@requests_mock.Mocker()
class TestSearchJSONInMemoryOutput(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/kobe.html"
        ), 'r') as file_input: self._html = file_input.read()
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/search/kobe.json",
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/search/kobe.json",
        )

    def test_in_memory_output(self, m):
        m.get(f"https://www.basketball-reference.com/search/search.fcgi?search=kobe",
              text=self._html,
              status_code=200)

        results = client.search(
            term="kobe",
            output_type=OutputType.JSON,
        )
        with open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.loads(results),
                json.load(expected_output_file),
            )


@requests_mock.Mocker()
class TestSearchCSVOutput(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/search/kobe.html"
        ), 'r') as file_input: self._html = file_input.read()
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/search/kobe.csv",
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/search/kobe.csv",
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def test_file_output(self, m):
        m.get(f"https://www.basketball-reference.com/search/search.fcgi?search=kobe",
              text=self._html,
              status_code=200)

        client.search(
            term="kobe",
            output_type=OutputType.CSV,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )

        self.assertTrue(
            filecmp.cmp(
                self.output_file_path,
                self.expected_output_file_path))
