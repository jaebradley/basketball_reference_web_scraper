from unittest import TestCase
from unittest.mock import patch, MagicMock

import requests
from requests.exceptions import HTTPError

import basketball_reference_web_scraper.client as client
from basketball_reference_web_scraper.errors import InvalidDate
from basketball_reference_web_scraper.http_service import HTTPService


class TestTeamBoxScores(TestCase):
    @patch.object(HTTPService, "team_box_scores")
    def test_invalid_date_error_raised_for_unknown_date(self, mocked_http_team_box_scores):
        mocked_http_team_box_scores.side_effect = HTTPError(
            response=MagicMock(status_code=requests.codes.not_found)
        )
        self.assertRaisesRegex(
            InvalidDate,
            "Date with year set to jae, month set to bae, and day set to bae is invalid",
            client.team_box_scores,
            day="bae",
            month="bae",
            year="jae"
        )
