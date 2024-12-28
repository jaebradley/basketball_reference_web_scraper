import os
from datetime import datetime, timedelta
from unittest import TestCase

import pytz
from lxml import html

from basketball_reference_web_scraper.data import Team, TEAM_NAME_TO_TEAM
from basketball_reference_web_scraper.html import SchedulePage
from basketball_reference_web_scraper.parsers import ScheduledGamesParser, TeamNameParser, ScheduledStartTimeParser


class BaseTest(TestCase):
    _path_from_schedule_directory: str = None

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(
                os.path.dirname(__file__),
                f"../files/schedule/{cls._path_from_schedule_directory}",
        ), 'r') as file_input: _html = file_input.read()
        cls._page = SchedulePage(html=html.fromstring(_html))

        super().setUpClass()


class BaseParserTest(BaseTest):

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(
                os.path.dirname(__file__),
                f"../files/schedule/{cls._path_from_schedule_directory}",
        ), 'r') as file_input: _html = file_input.read()
        cls._parsed_results = ScheduledGamesParser(
            start_time_parser=ScheduledStartTimeParser(),
            team_name_parser=TeamNameParser(team_names_to_teams=TEAM_NAME_TO_TEAM),
        ).parse_games(games=SchedulePage(html=html.fromstring(_html)).rows)

        super().setUpClass()


class TestSchedulePage(BaseTest):
    _path_from_schedule_directory = "2001/2001.html"

    def test_expected_urls(self):
        self.assertEqual(self._page.other_months_schedule_urls, [
            "/leagues/NBA_2001_games-october.html",
            "/leagues/NBA_2001_games-november.html",
            "/leagues/NBA_2001_games-december.html",
            "/leagues/NBA_2001_games-january.html",
            "/leagues/NBA_2001_games-february.html",
            "/leagues/NBA_2001_games-march.html",
            "/leagues/NBA_2001_games-april.html",
            "/leagues/NBA_2001_games-may.html",
            "/leagues/NBA_2001_games-june.html",
        ])


class TestOctober2001Parser(BaseParserTest):
    _path_from_schedule_directory = "2001/2001.html"

    def test_length(self):
        self.assertEqual(len(self._parsed_results), 13)

    def test_first_game(self):
        first_game = self._parsed_results[0]
        expected_datetime = pytz.timezone("US/Eastern") \
            .localize(datetime(year=2000, month=10, day=31, hour=19, minute=30)) \
            .astimezone(pytz.utc)

        self.assertTrue(abs(first_game["start_time"] - expected_datetime) < timedelta(seconds=1))
        self.assertEqual(first_game["away_team"], Team.CHARLOTTE_HORNETS)
        self.assertEqual(first_game["home_team"], Team.ATLANTA_HAWKS)
        self.assertEqual(first_game["away_team_score"], 106)
        self.assertEqual(first_game["home_team_score"], 82)


class TestOctober2018Parser(BaseParserTest):
    _path_from_schedule_directory = "2018/2018.html"

    def test_length(self):
        self.assertEqual(len(self._parsed_results), 104)


class TestParsingUpcomingGames(BaseParserTest):
    _path_from_schedule_directory = "upcoming-games.html"

    def test_length(self):
        self.assertEqual(len(self._parsed_results), 79)

    def test_first_game(self):
        first_game = self._parsed_results[0]

        self.assertEqual(first_game["start_time"],
                         pytz.timezone("US/Eastern") \
                         .localize(datetime(year=2019, month=4, day=1, hour=19, minute=30)) \
                         .astimezone(pytz.utc))
        self.assertEqual(first_game["away_team"], Team.MIAMI_HEAT)
        self.assertEqual(first_game["home_team"], Team.BOSTON_CELTICS)
        self.assertIsNone(first_game["away_team_score"])
        self.assertIsNone(first_game["home_team_score"])
