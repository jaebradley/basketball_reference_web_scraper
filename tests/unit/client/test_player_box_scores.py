from unittest import TestCase, mock

import requests_mock
from requests import HTTPError, codes

from basketball_reference_web_scraper.client import player_box_scores
from basketball_reference_web_scraper.errors import InvalidDate
from basketball_reference_web_scraper.http_service import HTTPService


class TestPlayerBoxScores(TestCase):
    @mock.patch.object(HTTPService, "player_box_scores")
    def test_raises_invalid_date_for_404_response(self, mocked_player_box_scores):
        mocked_player_box_scores.side_effect = HTTPError(
            response=mock.Mock(status_code=codes.not_found)
        )
        self.assertRaises(InvalidDate, player_box_scores, day=1, month=1, year=2018)

    @mock.patch.object(HTTPService, "player_box_scores")
    def test_raises_non_404_http_error(self, mocked_player_box_scores):
        mocked_player_box_scores.side_effect = HTTPError(
            response=mock.Mock(status_code=codes.server_error)
        )
        self.assertRaises(HTTPError, player_box_scores, day=1, month=1, year=2018)

    @requests_mock.Mocker()
    def test_raises_invalid_date_for_impossible_date_without_making_http_request(
        self, m
    ):
        with self.assertRaises(InvalidDate):
            player_box_scores(day=30, month=2, year=2021)
        self.assertEqual([], m.request_history)

    @requests_mock.Mocker()
    def test_raises_invalid_date_for_non_date_values_without_making_http_request(
        self, m
    ):
        with self.assertRaises(InvalidDate):
            player_box_scores(day="bae", month="bae", year="jae")
        self.assertEqual([], m.request_history)
