import requests_mock
from unittest import TestCase

from basketball_reference_web_scraper.client import playoff_player_box_scores
from basketball_reference_web_scraper.errors import InvalidPlayerAndSeason


class TestPlayerPlayoffBoxScores(TestCase):
    @requests_mock.Mocker()
    def test_raises_exception_for_empty_player_identifier_without_making_http_request(
        self, m
    ):
        with self.assertRaises(InvalidPlayerAndSeason):
            playoff_player_box_scores(player_identifier="", season_end_year=2000)
        self.assertEqual([], m.request_history)
