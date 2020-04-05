from unittest import TestCase, mock

from requests import HTTPError, codes

from basketball_reference_web_scraper.client import play_by_play
from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.errors import InvalidDate
from basketball_reference_web_scraper.http_service import HTTPService


class TestPlayByPlay(TestCase):
    @mock.patch.object(HTTPService, "play_by_play")
    def test_raises_invalid_date_for_404_response(self, mocked_play_by_play):
        mocked_play_by_play.side_effect = HTTPError(response=mock.Mock(status_code=codes.not_found))
        self.assertRaises(InvalidDate, play_by_play, home_team=Team.MILWAUKEE_BUCKS,  day=1, month=1, year=2018)

    @mock.patch.object(HTTPService, "play_by_play")
    def test_raises_non_404_http_error(self, mocked_play_by_play):
        mocked_play_by_play.side_effect = HTTPError(response=mock.Mock(status_code=codes.server_error))
        self.assertRaises(HTTPError, play_by_play, home_team=Team.MILWAUKEE_BUCKS,  day=1, month=1, year=2018)

