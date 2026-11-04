import os
from unittest import TestCase
from unittest.mock import patch

import requests_mock

from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.http_service import HTTPService
from basketball_reference_web_scraper.parser_service import ParserService


class TestCustomHTTPSettings(TestCase):
    def setUp(self):
        with open(
            os.path.join(
                os.path.dirname(__file__),
                "../files/players_season_totals/2018.html",
            ),
            "r",
        ) as fixture:
            self._html = fixture.read()
        self._url = "https://www.basketball-reference.com/leagues/NBA_2018_totals.html"

    @requests_mock.Mocker()
    def test_custom_user_agent_is_applied_to_request(self, m):
        m.get(self._url, text=self._html, status_code=200)

        client.players_season_totals(
            season_end_year=2018,
            headers={"User-Agent": "my-custom-user-agent/1.0"},
        )

        self.assertEqual(
            "my-custom-user-agent/1.0",
            m.last_request.headers.get("User-Agent"),
        )

    @requests_mock.Mocker()
    def test_custom_header_is_applied_to_request(self, m):
        m.get(self._url, text=self._html, status_code=200)

        client.players_season_totals(
            season_end_year=2018,
            headers={"X-Custom-Header": "custom-value"},
        )

        self.assertEqual(
            "custom-value",
            m.last_request.headers.get("X-Custom-Header"),
        )

    @requests_mock.Mocker()
    def test_default_user_agent_is_used_when_no_settings_provided(self, m):
        m.get(self._url, text=self._html, status_code=200)

        client.players_season_totals(season_end_year=2018)

        self.assertTrue(
            m.last_request.headers.get("User-Agent", "").startswith("python-requests/"),
        )


class TestHTTPServiceForwardsCustomSettings(TestCase):
    @patch("basketball_reference_web_scraper.http_service.requests.get")
    def test_headers_proxies_and_timeout_are_forwarded_to_requests(self, mock_get):
        headers = {"User-Agent": "my-custom-user-agent/1.0"}
        proxies = {"https": "https://proxy.example.com:8080"}

        service = HTTPService(
            parser=ParserService(),
            headers=headers,
            proxies=proxies,
            timeout=12,
        )
        service._get(url="https://www.basketball-reference.com/")

        _, kwargs = mock_get.call_args
        self.assertEqual(headers, kwargs["headers"])
        self.assertEqual(proxies, kwargs["proxies"])
        self.assertEqual(12, kwargs["timeout"])

    @patch("basketball_reference_web_scraper.http_service.requests.get")
    def test_settings_default_to_none_to_preserve_existing_behavior(self, mock_get):
        service = HTTPService(parser=ParserService())
        service._get(url="https://www.basketball-reference.com/")

        _, kwargs = mock_get.call_args
        self.assertIsNone(kwargs["headers"])
        self.assertIsNone(kwargs["proxies"])
        self.assertIsNone(kwargs["timeout"])
