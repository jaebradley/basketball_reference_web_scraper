import os
from datetime import datetime, timedelta
from unittest import TestCase

import pytz
import requests
from lxml import html

from basketball_reference_web_scraper.data import Team, TEAM_NAME_TO_TEAM
from basketball_reference_web_scraper.html import SchedulePage
from basketball_reference_web_scraper.parsers import ScheduledGamesParser, TeamNameParser, ScheduledStartTimeParser


class TestScheduleParser(TestCase):
    def setUp(self):
        self.october_2001_html = requests.get(
            'https://www.basketball-reference.com/leagues/NBA_2001_games.html'
        ).text
        self.october_2018_html = requests.get(
            'https://www.basketball-reference.com/leagues/NBA_2018_games-october.html'
        ).text
        self.schedule_with_future_games_html_file = open(
            os.path.join(os.path.dirname(__file__),
                         '../files/NBA_2019_games-april.html')
        )
        self.schedule_with_future_games_html = self.schedule_with_future_games_html_file.read()
        self.parser = ScheduledGamesParser(
            start_time_parser=ScheduledStartTimeParser(),
            team_name_parser=TeamNameParser(team_names_to_teams=TEAM_NAME_TO_TEAM),
        )

    def tearDown(self):
        self.schedule_with_future_games_html_file.close()

    def test_parse_october_2001_schedule_for_month_url_paths_(self):
        page = SchedulePage(html=html.fromstring(self.october_2001_html))
        expected_urls = [
            "/leagues/NBA_2001_games-november.html",
            "/leagues/NBA_2001_games-december.html",
            "/leagues/NBA_2001_games-january.html",
            "/leagues/NBA_2001_games-february.html",
            "/leagues/NBA_2001_games-march.html",
            "/leagues/NBA_2001_games-april.html",
            "/leagues/NBA_2001_games-may.html",
            "/leagues/NBA_2001_games-june.html",
        ]
        self.assertEqual(page.other_months_schedule_urls, expected_urls)

    def test_parse_october_2001_schedule(self):
        page = SchedulePage(html=html.fromstring(self.october_2001_html))
        parsed_schedule = self.parser.parse_games(games=page.rows)
        first_game = parsed_schedule[0]
        expected_datetime = pytz.timezone("US/Eastern") \
            .localize(datetime(year=2000, month=10, day=31, hour=19, minute=30)) \
            .astimezone(pytz.utc)

        self.assertEqual(len(parsed_schedule), 13)
        self.assertTrue(abs(first_game["start_time"] - expected_datetime) < timedelta(seconds=1))
        self.assertEqual(first_game["away_team"], Team.CHARLOTTE_HORNETS)
        self.assertEqual(first_game["home_team"], Team.ATLANTA_HAWKS)
        self.assertEqual(first_game["away_team_score"], 106)
        self.assertEqual(first_game["home_team_score"], 82)

    def test_parse_october_2018_schedule(self):
        page = SchedulePage(html=html.fromstring(self.october_2018_html))
        parsed_schedule = self.parser.parse_games(games=page.rows)
        self.assertEqual(len(parsed_schedule), 104)

    def test_parse_future_game(self):
        page = SchedulePage(html=html.fromstring(self.schedule_with_future_games_html))
        parsed_schedule = self.parser.parse_games(games=page.rows)
        first_game = parsed_schedule[0]
        expected_first_game_start_time = pytz.timezone("US/Eastern") \
            .localize(datetime(year=2019, month=4, day=1, hour=19, minute=30)) \
            .astimezone(pytz.utc)

        self.assertIsNotNone(parsed_schedule)
        self.assertEqual(len(parsed_schedule), 79)
        self.assertEqual(first_game["start_time"], expected_first_game_start_time)
        self.assertEqual(first_game["away_team"], Team.MIAMI_HEAT)
        self.assertEqual(first_game["home_team"], Team.BOSTON_CELTICS)
        self.assertIsNone(first_game["away_team_score"])
        self.assertIsNone(first_game["home_team_score"])
