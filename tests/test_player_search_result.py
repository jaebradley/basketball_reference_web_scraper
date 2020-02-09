from unittest import TestCase
from unittest.mock import patch, PropertyMock, MagicMock

from basketball_reference_web_scraper.html import PlayerSearchResult


class TestPlayerSearchResult(TestCase):
    def test_league_abbreviation_query(self):
        self.assertEqual(
            PlayerSearchResult(html=MagicMock()).league_abbreviation_query,
            './div[@class="search-item-league"]'
        )

    @patch.object(PlayerSearchResult, 'league_abbreviation_query', new_callable=PropertyMock)
    def test_league_abbreviations_are_none_when_no_matching_abbreviations(self, mocked_query):
        mocked_query.return_value = "some query"

        html = MagicMock()
        html.xpath = MagicMock(return_value=[])

        self.assertIsNone(PlayerSearchResult(html=html).league_abbreviations)
        html.xpath.assert_called_once_with("some query")

    @patch.object(PlayerSearchResult, 'league_abbreviation_query', new_callable=PropertyMock)
    def test_league_abbreviations_are_first_abbreviation_text_content_when__matching_abbreviations(self, mocked_query):
        mocked_query.return_value = "some query"
        first_abbreviation = MagicMock()
        first_abbreviation.text_content = MagicMock(return_value="first abbreviation")

        second_abbreviation = MagicMock()
        second_abbreviation.text_content = MagicMock(return_value="second abbreviation")

        html = MagicMock()
        html.xpath = MagicMock(return_value=[first_abbreviation, second_abbreviation])

        self.assertEqual(
            PlayerSearchResult(html=html).league_abbreviations,
            "first abbreviation",
        )
        html.xpath.assert_called_once_with("some query")
