import requests_mock
from requests import HTTPError, codes
from unittest import TestCase

from basketball_reference_web_scraper import client


class TestStandings(TestCase):
    @requests_mock.Mocker()
    def test_raises_http_error_for_redirect_response_with_empty_body(self, m):
        m.get(
            "https://www.basketball-reference.com/leagues/NBA_2020.html",
            status_code=301,
            text="",
            headers={
                "Location": "https://www.basketball-reference.com/leagues/NBA_2021.html"
            },
        )

        with self.assertRaises(HTTPError) as context:
            client.standings(season_end_year=2020)

        self.assertEqual(
            codes.moved_permanently, context.exception.response.status_code
        )
