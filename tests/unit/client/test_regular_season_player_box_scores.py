from unittest import TestCase
from unittest.mock import MagicMock, patch

from requests import HTTPError, codes

from basketball_reference_web_scraper.client import regular_season_player_box_scores
from basketball_reference_web_scraper.errors import InvalidPlayerAndSeason
from basketball_reference_web_scraper.http_service import HTTPService


class TestPlayerRegularSeasonBoxScores(TestCase):
    @patch.object(HTTPService, "regular_season_player_box_scores")
    def test_raises_exception_for_500_response(self, mocked_regular_season_player_box_scores):
        mocked_regular_season_player_box_scores.side_effect = HTTPError(
            response=MagicMock(status_code=codes.internal_server_error)
        )
        self.assertRaises(InvalidPlayerAndSeason, regular_season_player_box_scores, 'Mock Player', 2000)

    @patch.object(HTTPService, "regular_season_player_box_scores")
    def test_raises_exception_for_404_response(self, mocked_regular_season_player_box_scores):
        mocked_regular_season_player_box_scores.side_effect = HTTPError(
            response=MagicMock(status_code=codes.not_found)
        )
        self.assertRaises(InvalidPlayerAndSeason, regular_season_player_box_scores, 'Mock Player', 2000)

    @patch.object(HTTPService, "regular_season_player_box_scores")
    def test_raises_non_500_http_error(self, mocked_regular_season_player_box_scores):
        mocked_regular_season_player_box_scores.side_effect = HTTPError(response=MagicMock(status_code=codes.bad_request))
        self.assertRaises(HTTPError, regular_season_player_box_scores, 'Mock Player', 2000)
