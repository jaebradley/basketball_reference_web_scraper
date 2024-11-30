import json
import os
from datetime import date, datetime
from pathlib import Path
from unittest import TestCase

import pytz
import requests_mock

from basketball_reference_web_scraper.client import season_schedule
from basketball_reference_web_scraper.data import OutputType, Team
from basketball_reference_web_scraper.errors import InvalidSeason


class TestSeasonScheduleInMemoryOutput(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/schedule/2018/2018.html",
        ), 'r') as file_input: self._base_html = file_input.read();
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/schedule/2018/october.html",
        ), 'r') as file_input: self._october_html = file_input.read();

        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/schedule/2018/november.html",
        ), 'r') as file_input: self._november_html = file_input.read();

        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/schedule/2018/december.html",
        ), 'r') as file_input: self._december_html = file_input.read();

        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/schedule/2018/january.html",
        ), 'r') as file_input: self._january_html = file_input.read();

        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/schedule/2018/february.html",
        ), 'r') as file_input: self._february_html = file_input.read();

        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/schedule/2018/march.html",
        ), 'r') as file_input: self._march_html = file_input.read();

        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/schedule/2018/april.html",
        ), 'r') as file_input: self._april_html = file_input.read();

        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/schedule/2018/may.html",
        ), 'r') as file_input: self._may_html = file_input.read();

        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/schedule/2018/june.html",
        ), 'r') as file_input: self._june_html = file_input.read();

    @requests_mock.Mocker()
    def test_2018_season_schedule_length(self, m):
        m.get("https://www.basketball-reference.com/leagues/NBA_2018_games.html", text=self._base_html, status_code=200)
        m.get("https://www.basketball-reference.com/leagues/NBA_2018_games-october.html",
              text=self._october_html,
              status_code=200)
        m.get("https://www.basketball-reference.com/leagues/NBA_2018_games-november.html",
              text=self._november_html,
              status_code=200)
        m.get("https://www.basketball-reference.com/leagues/NBA_2018_games-december.html",
              text=self._december_html,
              status_code=200)
        m.get("https://www.basketball-reference.com/leagues/NBA_2018_games-january.html",
              text=self._january_html,
              status_code=200)
        m.get("https://www.basketball-reference.com/leagues/NBA_2018_games-february.html",
              text=self._february_html,
              status_code=200)
        m.get("https://www.basketball-reference.com/leagues/NBA_2018_games-march.html",
              text=self._march_html,
              status_code=200)
        m.get("https://www.basketball-reference.com/leagues/NBA_2018_games-april.html",
              text=self._april_html,
              status_code=200)
        m.get("https://www.basketball-reference.com/leagues/NBA_2018_games-may.html",
              text=self._may_html,
              status_code=200)
        m.get("https://www.basketball-reference.com/leagues/NBA_2018_games-june.html",
              text=self._june_html,
              status_code=200)
        result = season_schedule(season_end_year=2018)
        self.assertEqual(1416, len(result))

    def test_first_game_of_2018_season(self):
        result = season_schedule(season_end_year=2018)
        self.assertEqual(
            result[0],
            {
                "away_team": Team.BOSTON_CELTICS,
                "away_team_score": 99,
                "home_team": Team.CLEVELAND_CAVALIERS,
                "home_team_score": 102,
                "start_time": datetime(2017, 10, 18, 0, 1, tzinfo=pytz.utc),
            },
        )

    def test_last_game_of_2018_season(self):
        result = season_schedule(season_end_year=2018)
        self.assertEqual(
            result[1311],
            {
                "away_team": Team.GOLDEN_STATE_WARRIORS,
                "away_team_score": 108,
                "home_team": Team.CLEVELAND_CAVALIERS,
                "home_team_score": 85,
                "start_time": datetime(2018, 6, 9, 1, 0, tzinfo=pytz.utc)
            }
        )

    def test_future_season_schedule_throws_invalid_season_error(self):
        current_year = date.today().year
        future_year = current_year + 10
        expected_message = "Season end year of {future_year} is invalid".format(future_year=future_year)
        self.assertRaisesRegex(
            InvalidSeason,
            expected_message,
            season_schedule,
            season_end_year=future_year
        )


class TestSeasonScheduleCSVOutput(TestCase):
    def setUp(self):
        self.output_2018_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/2018_season_schedule.csv"
        )
        self.expected_output_2018_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2018_season_schedule.csv"
        )
        self.output_2001_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/2001_season_schedule.csv"
        )
        self.expected_output_2001_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2001_season_schedule.csv"
        )

    def tearDown(self):
        if Path(self.output_2018_file_path).exists():
            os.remove(self.output_2018_file_path)

        if Path(self.output_2001_file_path).exists():
            os.remove(self.output_2001_file_path)

    def test_2018_season_schedule_csv(self):
        season_schedule(season_end_year=2018, output_type=OutputType.CSV, output_file_path=self.output_2018_file_path)
        with open(self.output_2018_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_2018_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                output_file.readlines(),
                expected_output_file.readlines()
            )

    def test_2001_season_schedule_csv(self):
        season_schedule(season_end_year=2001, output_type=OutputType.CSV, output_file_path=self.output_2001_file_path)
        with open(self.output_2001_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_2001_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                output_file.readlines(),
                expected_output_file.readlines()
            )


class TestSeasonScheduleJSONOutput(TestCase):
    def setUp(self):
        self.output_2018_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/2018_season_schedule.json"
        )
        self.expected_output_2018_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2018_season_schedule.json"
        )
        self.output_2001_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/2001_season_schedule.json"
        )
        self.expected_output_2001_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2001_season_schedule.json"
        )

    def tearDown(self):
        if Path(self.output_2018_file_path).exists():
            os.remove(self.output_2018_file_path)

        if Path(self.output_2001_file_path).exists():
            os.remove(self.output_2001_file_path)

    def test_2018_season_schedule_in_memory_json(self):
        result = season_schedule(season_end_year=2018, output_type=OutputType.JSON)
        with open(self.expected_output_2018_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.loads(result),
                json.load(expected_output_file)
            )

    def test_writing_2018_season_schedule_json_file(self):
        season_schedule(season_end_year=2018, output_type=OutputType.JSON, output_file_path=self.output_2018_file_path)
        with open(self.output_2018_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_2018_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.load(output_file),
                json.load(expected_output_file),
            )

    def test_writing_2001_season_schedule_json_file(self):
        season_schedule(season_end_year=2001, output_type=OutputType.JSON, output_file_path=self.output_2001_file_path)
        with open(self.output_2001_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_2001_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.load(output_file),
                json.load(expected_output_file),
            )
