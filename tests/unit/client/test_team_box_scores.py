from unittest import TestCase
from unittest.mock import patch, MagicMock

import requests
import requests_mock
from requests.exceptions import HTTPError

import basketball_reference_web_scraper.client as client
from basketball_reference_web_scraper.errors import InvalidDate
from basketball_reference_web_scraper.http_service import HTTPService
from basketball_reference_web_scraper.parser_service import ParserService


class TestTeamBoxScores(TestCase):
    @patch.object(HTTPService, "team_box_scores")
    def test_invalid_date_error_raised_for_unknown_date(
        self, mocked_http_team_box_scores
    ):
        mocked_http_team_box_scores.side_effect = HTTPError(
            response=MagicMock(status_code=requests.codes.not_found)
        )
        self.assertRaisesRegex(
            InvalidDate,
            "Date with year set to jae, month set to bae, and day set to bae is invalid",
            client.team_box_scores,
            day="bae",
            month="bae",
            year="jae",
        )

    @requests_mock.Mocker()
    def test_raises_invalid_date_for_impossible_date_without_making_http_request(
        self, m
    ):
        with self.assertRaises(InvalidDate):
            client.team_box_scores(day=30, month=2, year=2021)
        self.assertEqual([], m.request_history)

    @requests_mock.Mocker()
    def test_raises_value_error_for_game_page_without_two_teams_statistics_tables(
        self, m
    ):
        m.get(
            "https://www.basketball-reference.com/boxscores/202001010ATL.html",
            text="<html><body>No statistics tables</body></html>",
        )

        with self.assertRaisesRegex(ValueError, "boxscores/202001010ATL.html"):
            HTTPService(parser=ParserService()).team_box_score(
                game_url_path="boxscores/202001010ATL.html"
            )
