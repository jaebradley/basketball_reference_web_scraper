from unittest import TestCase, mock

from requests import codes

from basketball_reference_web_scraper.errors import InvalidDate
from basketball_reference_web_scraper.http_service import HTTPService


class TestHTTPService(TestCase):
    @mock.patch("requests.get")
    def test_player_box_scores_raises_invalid_date_for_300_response(self, mocked_get):
        response = mock.Mock(status_code=codes.multiple_choices)
        mocked_get.return_value = response
        self.assertRaisesRegex(
            InvalidDate,
            "Date with year set to 2018, month set to 1, and day set to 1 is invalid",
            HTTPService(parser=mock.MagicMock()).player_box_scores,
            day=1, month=1, year=2018)
