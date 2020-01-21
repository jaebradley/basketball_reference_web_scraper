import os
from datetime import datetime, timedelta
from unittest import TestCase

import pytz
from lxml import html

from basketball_reference_web_scraper.data import Team, TEAM_NAME_TO_TEAM
from basketball_reference_web_scraper.html import SchedulePage
from basketball_reference_web_scraper.parsers import ScheduledGamesParser, TeamNameParser, ScheduledStartTimeParser

october_2001_schedule_html = os.path.join(os.path.dirname(__file__), './NBA_2001_games-october.html')
october_2018_schedule_html = os.path.join(os.path.dirname(__file__), './NBA_2018_games-october.html')
april_2019_schedule_html = os.path.join(os.path.dirname(__file__), './NBA_2019_games-april.html')


class TestScheduleParser(TestCase):
    def setUp(self):
        self.october_2001_html_file = open(october_2001_schedule_html)
        self.october_2018_html_file = open(october_2018_schedule_html)
        self.april_2019_html_file = open(april_2019_schedule_html)
        self.october_2001_html = self.october_2001_html_file.read()
        self.october_2018_html = self.october_2018_html_file.read()
        self.april_2019_html = self.april_2019_html_file.read()
        self.parser = ScheduledGamesParser(
            start_time_parser=ScheduledStartTimeParser(),
            team_name_parser=TeamNameParser(team_names_to_teams=TEAM_NAME_TO_TEAM),
        )

    def tearDown(self):
        self.october_2001_html_file.close()
        self.october_2018_html_file.close()
        self.april_2019_html_file.close()

    def test_parse_october_2001_schedule_for_month_url_paths_(self):
        page = SchedulePage(html=html.fromstring(self.october_2001_html))
        expected_urls = [
            "https://www.basketball-reference.com/leagues/NBA_2001_games-november.html",
            "https://www.basketball-reference.com/leagues/NBA_2001_games-december.html",
            "https://www.basketball-reference.com/leagues/NBA_2001_games-january.html",
            "https://www.basketball-reference.com/leagues/NBA_2001_games-february.html",
            "https://www.basketball-reference.com/leagues/NBA_2001_games-march.html",
            "https://www.basketball-reference.com/leagues/NBA_2001_games-april.html",
            "https://www.basketball-reference.com/leagues/NBA_2001_games-may.html",
            "https://www.basketball-reference.com/leagues/NBA_2001_games-june.html",
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
        page = SchedulePage(html=html.fromstring(self.april_2019_html))
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
