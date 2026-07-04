import os
from unittest import TestCase

import requests_mock
from basketball_reference_web_scraper.client import players_regular_season_shooting_statistics
from basketball_reference_web_scraper.errors import InvalidSeason


class Test2026(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/players_season_shooting_statistics/2026.html",
        ), 'r') as file_input: self._html = file_input.read();

    @requests_mock.Mocker()
    def test_length(self, m):
        m.get("https://www.basketball-reference.com/leagues/NBA_2026_shooting.html", text=self._html, status_code=200)
        result = players_regular_season_shooting_statistics(season_end_year=2026)
        self.assertEqual(len(result), 661)
        self.assertEqual(result[660]["name"], "Darius Brown II")


class Test2025(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/players_season_shooting_statistics/2025.html",
        ), 'r') as file_input: self._html = file_input.read();

    @requests_mock.Mocker()
    def test_length(self, m):
        m.get("https://www.basketball-reference.com/leagues/NBA_2025_shooting.html", text=self._html, status_code=200)
        result = players_regular_season_shooting_statistics(season_end_year=2025)
        self.assertEqual(len(result), 654)
        self.assertEqual(result[653]["name"], "Jahlil Okafor")


class TestInvalidSeason(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/players_season_shooting_statistics/not_found.html",
        ), 'r') as file_input: self._html = file_input.read();

    @requests_mock.Mocker()
    def test_invalid_season(self, m):
        m.get("https://www.basketball-reference.com/leagues/NBA_2026_shooting.html", text=self._html, status_code=404)
        self.assertRaisesRegex(InvalidSeason, f"Season end year of 2026 is invalid",
                               players_regular_season_shooting_statistics,
                               season_end_year=2026)
