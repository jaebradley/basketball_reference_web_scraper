from unittest import TestCase, mock

from requests import HTTPError, codes

from basketball_reference_web_scraper.client import play_by_play
from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.errors import InvalidDate


class TestPlayByPlay(TestCase):
    @mock.patch("basketball_reference_web_scraper.client.http_client")
    def test_raises_invalid_date_for_404_response(self, mocked_http_client):
        mocked_http_client.play_by_play.side_effect = HTTPError(response=mock.Mock(status_code=codes.not_found))
        self.assertRaises(InvalidDate, play_by_play, home_team=Team.MILWAUKEE_BUCKS,  day=1, month=1, year=2018)

    @mock.patch("basketball_reference_web_scraper.client.http_client")
    def test_raises_non_404_http_error(self, mocked_http_client):
        mocked_http_client.play_by_play.side_effect = HTTPError(response=mock.Mock(status_code=codes.server_error))
        self.assertRaises(HTTPError, play_by_play, home_team=Team.MILWAUKEE_BUCKS,  day=1, month=1, year=2018)

