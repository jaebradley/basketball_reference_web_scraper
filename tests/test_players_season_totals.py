from unittest import TestCase

from basketball_reference_web_scraper.client import players_season_totals
from basketball_reference_web_scraper.data import OutputType, OutputWriteOption


class TestPlayerSeasonTotals(TestCase):
    def test_players_season_totals(self):
        result = players_season_totals(season_end_year=2018)
        self.assertIsNotNone(result)

    def test_players_season_totals_json(self):
        result = players_season_totals(season_end_year=2018, output_type=OutputType.JSON)
        self.assertIsNotNone(result)

    def test_players_season_totals_csv(self):
        players_season_totals(season_end_year=2018, output_type=OutputType.CSV, output_file_path="./player_season_totals_2018.csv")

    def test_players_season_totals_csv_append(self):
        players_season_totals(season_end_year=2018, output_type=OutputType.CSV, output_file_path="./player_season_totals_2018.csv", output_write_option=OutputWriteOption.APPEND)

    def test_2001_players_season_totals_csv(self):
        players_season_totals(season_end_year=2001, output_type=OutputType.CSV, output_file_path="./player_season_totals_2001.csv", output_write_option=OutputWriteOption.WRITE)
