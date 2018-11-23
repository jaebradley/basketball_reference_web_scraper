from datetime import date
from unittest import TestCase, mock

from requests import HTTPError, codes

from basketball_reference_web_scraper.client import season_schedule
from basketball_reference_web_scraper.data import OutputType, OutputWriteOption
from basketball_reference_web_scraper.errors import InvalidSeason


class TestSeasonSchedule(TestCase):
    def test_season_schedule(self):
        result = season_schedule(season_end_year=2018)
        self.assertIsNotNone(result)

    def test_season_schedule_json(self):
        result = season_schedule(season_end_year=2018, output_type=OutputType.JSON)
        self.assertIsNotNone(result)

    def test_season_schedule_csv(self):
        season_schedule(season_end_year=2018, output_type=OutputType.CSV, output_file_path="./foo.csv")

    def test_season_schedule_csv_append(self):
        season_schedule(season_end_year=2018, output_type=OutputType.CSV, output_file_path="./foo.csv", output_write_option=OutputWriteOption.WRITE)

    def test_2017_season_schedule_csv_append(self):
        season_schedule(season_end_year=2001, output_type=OutputType.CSV, output_file_path="./foo.csv", output_write_option=OutputWriteOption.WRITE)

    def test_future_season_schedule_throws_invalid_season_error(self):
        current_year = date.today().year
        future_year = current_year + 10
        expected_message = "Season end year of {future_year} is invalid".format(future_year=future_year)
        self.assertRaisesRegex(InvalidSeason, expected_message, season_schedule, season_end_year=future_year)

    @mock.patch("basketball_reference_web_scraper.client.http_client")
    def test_not_found_raises_invalid_season(self, mocked_http_client):
        end_year = "jaebaebae"
        expected_message = "Season end year of {end_year} is invalid".format(end_year=end_year)
        mocked_http_client.season_schedule.side_effect = HTTPError(response=mock.Mock(status_code=codes.not_found))
        self.assertRaisesRegex(InvalidSeason, expected_message, season_schedule, season_end_year=end_year)

    @mock.patch("basketball_reference_web_scraper.client.http_client")
    def test_other_http_error_is_raised(self, mocked_http_client):
        mocked_http_client.season_schedule.side_effect = HTTPError(
            response=mock.Mock(status_code=codes.internal_server_error))
        self.assertRaises(HTTPError, season_schedule, season_end_year=2018)
