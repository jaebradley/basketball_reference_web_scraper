from datetime import date
from unittest import TestCase, mock
import os

from requests import HTTPError, codes

from basketball_reference_web_scraper.client import players_season_totals
from basketball_reference_web_scraper.data import OutputType, OutputWriteOption
from basketball_reference_web_scraper.errors import InvalidSeason


class TestPlayerSeasonTotals(TestCase):

    def test_players_season_totals(self):
        result = players_season_totals(season_end_year=2018)
        self.assertIsNotNone(result)

    def test_players_season_totals_json(self):
        result = players_season_totals(season_end_year=2018, output_type=OutputType.JSON)
        self.assertIsNotNone(result)

    def test_players_season_totals_csv(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/player_season_totals_2018.csv",
        )
        players_season_totals(season_end_year=2018, output_type=OutputType.CSV, output_file_path=output_file_path)

    def test_players_season_totals_csv_append(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/player_season_totals_2018.csv",
        )
        players_season_totals(season_end_year=2018, output_type=OutputType.CSV,
                              output_file_path=output_file_path, output_write_option=OutputWriteOption.APPEND)

    def test_2001_players_season_totals_csv(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/player_season_totals_2001.csv",
        )
        players_season_totals(season_end_year=2001, output_type=OutputType.CSV, output_file_path=output_file_path,
                              output_write_option=OutputWriteOption.WRITE)

    def test_future_season_raises_invalid_season(self):
        current_year = date.today().year
        future_year = current_year + 10
        expected_message = "Season end year of {future_year} is invalid".format(future_year=future_year)
        self.assertRaisesRegex(InvalidSeason, expected_message, players_season_totals, season_end_year=future_year)

    @mock.patch("basketball_reference_web_scraper.client.http_client")
    def test_not_found_raises_invalid_season(self, mocked_http_client):
        end_year = "jaebaebae"
        expected_message = "Season end year of {end_year} is invalid".format(end_year=end_year)
        mocked_http_client.players_season_totals.side_effect = HTTPError(response=mock.Mock(status_code=codes.not_found))
        self.assertRaisesRegex(InvalidSeason, expected_message, players_season_totals, season_end_year=end_year)

    @mock.patch("basketball_reference_web_scraper.client.http_client")
    def test_other_http_error_is_raised(self, mocked_http_client):
        mocked_http_client.players_season_totals.side_effect = HTTPError(response=mock.Mock(status_code=codes.internal_server_error))
        self.assertRaises(HTTPError, players_season_totals, season_end_year=2018)
