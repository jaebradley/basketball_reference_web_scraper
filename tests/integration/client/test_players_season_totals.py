import json
import os
from datetime import date
from unittest import TestCase

from basketball_reference_web_scraper.client import players_season_totals
from basketball_reference_web_scraper.data import OutputType, OutputWriteOption
from basketball_reference_web_scraper.errors import InvalidSeason


class BaseTestPlayerSeasonTotalsJSONFileOutput(TestCase):
    @property
    def year(self):
        raise NotImplementedError

    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/player_season_totals_{year}.json".format(year=self.year),
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/player_season_totals_{year}.json".format(year=self.year)
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def assert_player_season_totals_file(self):
        players_season_totals(
            season_end_year=self.year,
            output_type=OutputType.JSON,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )
        with open(self.output_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.load(output_file),
                json.load(expected_output_file),
            )


class BaseTestPlayerSeasonTotalsCSVFileOutput(TestCase):
    @property
    def year(self):
        raise NotImplementedError

    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/player_season_totals_{year}.csv".format(year=self.year),
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/player_season_totals_{year}.csv".format(year=self.year)
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def assert_player_season_totals_file(self):
        players_season_totals(
            season_end_year=self.year,
            output_type=OutputType.CSV,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )
        with open(self.output_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                output_file.readlines(),
                expected_output_file.readlines(),
            )


class TestPlayerSeasonTotalsInMemory(TestCase):
    def test_2018_players_season_totals_length(self):
        result = players_season_totals(season_end_year=2018)
        self.assertEqual(len(result), 605)

    def test_future_season_raises_invalid_season(self):
        current_year = date.today().year
        future_year = current_year + 10
        expected_message = "Season end year of {future_year} is invalid".format(future_year=future_year)
        self.assertRaisesRegex(InvalidSeason, expected_message, players_season_totals, season_end_year=future_year)


class Test2018PlayerSeasonTotalsInMemoryJSONOutput(TestCase):
    def setUp(self):
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/player_season_totals_2018.json"
        )

    def test_players_season_totals_json(self):
        result = players_season_totals(season_end_year=2018, output_type=OutputType.JSON)
        with open(self.expected_output_file_path, "r", encoding="utf8") as expected_results_file:
            self.assertEqual(
                json.loads(result),
                json.load(expected_results_file)
            )


class Test2018PlayerSeasonTotalsCSVFileOutput(BaseTestPlayerSeasonTotalsCSVFileOutput):
    @property
    def year(self):
        return 2018

    def test_2018_player_season_totals_file(self):
        self.assert_player_season_totals_file()


class Test2001PlayerSeasonTotalsCSVFileOutput(BaseTestPlayerSeasonTotalsCSVFileOutput):
    @property
    def year(self):
        return 2001

    def test_2001_player_season_totals_file(self):
        self.assert_player_season_totals_file()


class Test2018PlayerSeasonTotalsJSONFileOutput(BaseTestPlayerSeasonTotalsJSONFileOutput):
    @property
    def year(self):
        return 2018

    def test_2018_player_season_totals_file(self):
        self.assert_player_season_totals_file()

