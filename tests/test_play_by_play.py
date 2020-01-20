from unittest import TestCase, mock

from requests import HTTPError, codes

from basketball_reference_web_scraper.client import play_by_play
from basketball_reference_web_scraper.data import OutputType, OutputWriteOption
from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.errors import InvalidDate


class TestPlayByPlay(TestCase):
    def test_get_play_by_play(self):
        result = play_by_play(home_team=Team.MILWAUKEE_BUCKS, day=27, month=10, year=2018)
        self.assertIsNotNone(result)

    def test_get_play_by_play_single_digit_month_and_day(self):
        result = play_by_play(home_team=Team.DENVER_NUGGETS, day=1, month=1, year=2019)
        self.assertIsNotNone(result)

    def test_get_play_by_play_for_day_that_does_not_exist(self):
        self.assertRaisesRegex(
            InvalidDate,
            "Date with year set to 2018, month set to 1, and day set to -1 is invalid",
            play_by_play,
            home_team=Team.MILWAUKEE_BUCKS, day=-1, month=1, year=2018)

    def test_get_box_scores_from_2003_csv(self):
        result = play_by_play(
            home_team=Team.TORONTO_RAPTORS, day=29, month=10, year=2003,
            output_type=OutputType.CSV, output_file_path="./foo.csv", output_write_option=OutputWriteOption.WRITE)

    def test_get_box_scores_from_2003_json(self):
        result = play_by_play(
            home_team=Team.TORONTO_RAPTORS, day=29, month=10, year=2003,
            output_type=OutputType.JSON, output_file_path="./foobar.json", output_write_option=OutputWriteOption.WRITE)

    def test_raises_invalid_date_for_nonexistent_dates(self):
        self.assertRaisesRegex(
            InvalidDate,
            "Date with year set to baz, month set to bar, and day set to foo is invalid",
            play_by_play,
            home_team=Team.MILWAUKEE_BUCKS, day="foo", month="bar", year="baz")

    @mock.patch("basketball_reference_web_scraper.client.http_client")
    def test_raises_invalid_date_for_404_response(self, mocked_http_client):
        mocked_http_client.play_by_play.side_effect = HTTPError(response=mock.Mock(status_code=codes.not_found))
        self.assertRaises(InvalidDate, play_by_play, home_team=Team.MILWAUKEE_BUCKS,  day=1, month=1, year=2018)

    @mock.patch("basketball_reference_web_scraper.client.http_client")
    def test_raises_non_404_http_error(self, mocked_http_client):
        mocked_http_client.play_by_play.side_effect = HTTPError(response=mock.Mock(status_code=codes.server_error))
        self.assertRaises(HTTPError, play_by_play, home_team=Team.MILWAUKEE_BUCKS,  day=1, month=1, year=2018)

    def test_non_unicode_matches(self):
        result = play_by_play(home_team=Team.GOLDEN_STATE_WARRIORS, day=16, month=10, year=2018)
        self.assertIsNotNone(result)