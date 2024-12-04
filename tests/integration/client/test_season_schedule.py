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


class SeasonScheduleMocker:
    def __init__(self, schedules_directory, season_end_year):
        html_files_directory = os.path.join(schedules_directory, str(season_end_year))
        self.responses_by_url = {}
        for file in os.listdir(os.fsencode(html_files_directory)):
            filename = os.fsdecode(file)
            if not filename.endswith(".html"):
                raise ValueError(
                    f"Unexpected prefix for {filename}. Expected all files in {html_files_directory} to end with .html.")

            with open(os.path.join(html_files_directory, filename), 'r') as file_input:
                if filename.startswith(str(season_end_year)):
                    key = f"https://www.basketball-reference.com/leagues/NBA_{season_end_year}_games.html"
                else:
                    key = f"https://www.basketball-reference.com/leagues/NBA_{season_end_year}_games-{filename}"
                self.responses_by_url[key] = file_input.read()

    def setup(self, m):
        for url, response in self.responses_by_url.items():
            m.get(url, text=response, status_code=200)


class TestSeasonScheduleInMemoryOutput(TestCase):
    def setUp(self):
        self.mocker = SeasonScheduleMocker(
            schedules_directory=os.path.join(
                os.path.dirname(__file__),
                "../files/schedule",
            ),
            season_end_year=2018
        )

    @requests_mock.Mocker()
    def test_2018_season_schedule_length(self, m):
        self.mocker.setup(m)
        result = season_schedule(season_end_year=2018)
        self.assertEqual(1416, len(result))

    @requests_mock.Mocker()
    def test_first_game_of_2018_season(self, m):
        self.mocker.setup(m)
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

    @requests_mock.Mocker()
    def test_last_game_of_2018_season(self, m):
        self.mocker.setup(m)
        result = season_schedule(season_end_year=2018)
        self.assertEqual(
            result[1415],
            {
                "away_team": Team.GOLDEN_STATE_WARRIORS,
                "away_team_score": 108,
                "home_team": Team.CLEVELAND_CAVALIERS,
                "home_team_score": 85,
                "start_time": datetime(2018, 6, 9, 1, 0, tzinfo=pytz.utc)
            }
        )


class TestFutureSeasonSchedule(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                f"../files/schedule/not-found.html",
        ), 'r') as file_input: self._html = file_input.read()

    @requests_mock.Mocker()
    def test_future_season_schedule_returns_empty_list(self, m):
        m.get(url=f"https://www.basketball-reference.com/leagues/NBA_2026_games.html", text=self._html, status_code=200)
        result = season_schedule(season_end_year=2026)
        self.assertEqual([], result)


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
