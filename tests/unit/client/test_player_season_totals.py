from unittest import TestCase
from unittest.mock import MagicMock, patch

from requests import HTTPError, codes

from basketball_reference_web_scraper.client import players_season_totals
from basketball_reference_web_scraper.errors import InvalidSeason
from basketball_reference_web_scraper.http_service import HTTPService


class TestPlayerSeasonTotals(TestCase):
    @patch.object(HTTPService, 'players_season_totals')
    def test_not_found_raises_invalid_season(self, mocked_players_season_totals):
        end_year = "jaebaebae"
        expected_message = "Season end year of {end_year} is invalid".format(end_year=end_year)
        mocked_players_season_totals.side_effect = HTTPError(response=MagicMock(status_code=codes.not_found))
        self.assertRaisesRegex(InvalidSeason, expected_message, players_season_totals, season_end_year=end_year)

    @patch.object(HTTPService, 'players_season_totals')
    def test_other_http_error_is_raised(self, mocked_players_season_totals):
        mocked_players_season_totals.side_effect = HTTPError(
            response=MagicMock(status_code=codes.internal_server_error)
        )
        self.assertRaises(HTTPError, players_season_totals, season_end_year=2018)
