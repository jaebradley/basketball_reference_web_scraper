import os
from datetime import date
from unittest import TestCase

from basketball_reference_web_scraper.client import players_advanced_season_totals
from basketball_reference_web_scraper.data import OutputType
from basketball_reference_web_scraper.errors import InvalidSeason


class BaseTestPlayerAdvancedSeasonTotalsCSVOutput(TestCase):
    @property
    def year(self):
        raise NotImplementedError

    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/player_advanced_season_totals_{year}.csv".format(year=self.year),
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/player_advanced_season_totals_{year}.csv".format(year=self.year),
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def assert_player_advanced_season_totals_csv(self):
        players_advanced_season_totals(
            season_end_year=self.year,
            output_type=OutputType.CSV,
            output_file_path=self.output_file_path,
        )

        with open(self.output_file_path, "r") as output_file, \
                open(self.expected_output_file_path, "r") as expected_output_file:
            self.assertEqual(
                output_file.readlines(),
                expected_output_file.readlines(),
            )


class Test2018PlayerAdvancedSeasonTotalsCSVOutput(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2018

    def test_players_advanced_season_totals_csv(self):
        self.assert_player_advanced_season_totals_csv()


class Test2001PlayerAdvancedSeasonTotalsCSVOutput(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2001

    def test_players_advanced_season_totals_csv(self):
        self.assert_player_advanced_season_totals_csv()


class TestPlayerAdvancedSeasonTotalsInMemoryOutput(TestCase):
    def test_future_season_raises_invalid_season(self):
        current_year = date.today().year
        future_year = current_year + 10
        expected_message = "Season end year of {future_year} is invalid".format(future_year=future_year)
        self.assertRaisesRegex(InvalidSeason, expected_message, players_advanced_season_totals, season_end_year=future_year)

    def test_players_advanced_season_totals(self):
        result = players_advanced_season_totals(season_end_year=2018)
        self.assertIsNotNone(result)

    def test_players_advanced_season_totals_json(self):
        result = players_advanced_season_totals(season_end_year=2018, output_type=OutputType.JSON)
        self.assertIsNotNone(result)
