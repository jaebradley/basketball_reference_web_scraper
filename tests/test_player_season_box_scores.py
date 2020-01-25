from unittest import TestCase, mock

from requests import HTTPError, codes

from basketball_reference_web_scraper.client import player_season_box_scores
from basketball_reference_web_scraper.errors import InvalidPlayer


class TestPlayerSeasonBoxScores(TestCase):
    def test_get_season_box_scores(self):
        try:
            result = player_season_box_scores('Russell Westbrook', 2020)
            self.assertIsNotNone(result)
        except (InvalidPlayer, HTTPError):
            self.fail('Exception was raised unexpectedly')

    def test_get_season_box_scores_for_player_that_does_not_exist(self):
        self.assertRaisesRegex(
            InvalidPlayer,
            'Player "Foo Bar" is invalid',
            player_season_box_scores,
            'Foo Bar', 2020)

    def test_get_season_box_scores_for_invalid_season(self):
        # bbref won't actually 404 or 500 if the season is invalid, it'll
        # just take you to the player page with blank data
        try:
            result = player_season_box_scores('Russell Westbrook', 3000)
            self.assertFalse(result)
        except (InvalidPlayer, HTTPError):
            self.fail('Exception was raised unexpectedly')

    def test_get_season_box_scores_for_player_with_punctuation(self):
        try:
            result = player_season_box_scores('D\'Angelo Russell', 2020)
            self.assertIsNotNone(result)
        except (InvalidPlayer, HTTPError):
            self.fail('Exception was raised unexpectedly')

    def test_get_season_box_scores_for_clint_capela(self):
        # Capela is a special case on basketball-reference.com where his
        # url was mistakenly generated incorrectly
        try:
            result = player_season_box_scores('Clint Capela', 2020)
            self.assertIsNotNone(result)
        except (InvalidPlayer, HTTPError):
            self.fail('Exception was raised unexpectedly')

    @mock.patch("basketball_reference_web_scraper.client.http_client")
    def test_raises_exception_for_500_response(self, mocked_http_client):
        mocked_http_client.player_season_box_scores.side_effect = HTTPError(response=mock.Mock(status_code=codes.internal_server_error))
        self.assertRaises(InvalidPlayer, player_season_box_scores, 'Mock Player', 2000)

    @mock.patch("basketball_reference_web_scraper.client.http_client")
    def test_raises_non_500_http_error(self, mocked_http_client):
        mocked_http_client.player_season_box_scores.side_effect = HTTPError(response=mock.Mock(status_code=codes.not_found))
        self.assertRaises(HTTPError, player_season_box_scores, 'Mock Player', 2000)
