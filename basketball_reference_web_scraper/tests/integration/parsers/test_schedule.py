from unittest import TestCase
from datetime import datetime, timedelta
import pytz
import os

from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.parsers import schedule

october_2001_schedule_html = os.path.join(os.path.dirname(__file__), './NBA_2001_games-october.html')
october_2018_schedule_html = os.path.join(os.path.dirname(__file__), './NBA_2018_games-october.html')


class TestSchedule(TestCase):
    def setUp(self):
        self.october_2001_html = open(october_2001_schedule_html).read()
        self.october_2018_html = open(october_2018_schedule_html).read()

    def test_parse_october_2001_schedule_for_month_url_paths_(self):
        urls = schedule.parse_schedule_for_month_url_paths(self.october_2001_html)
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
        self.assertIsNotNone(urls)
        self.assertEqual(urls, expected_urls)

    def test_parse_october_2001_schedule(self):
        parsed_schedule = schedule.parse_schedule(self.october_2001_html)
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
        parsed_schedule = schedule.parse_schedule(self.october_2018_html)
        self.assertEqual(len(parsed_schedule), 104)
