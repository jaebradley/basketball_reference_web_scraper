from unittest import TestCase
from unittest.mock import MagicMock

from basketball_reference_web_scraper.html import PlayerPageTotalsRow


class TestPlayerPageTotalsRow(TestCase):
    def test_league_abbreviation_is_none_when_no_matching_league_abbreviations(self):
        html = MagicMock()
        html.xpath = MagicMock(return_value=[])

        self.assertIsNone(PlayerPageTotalsRow(html=html).league_abbreviation)
        html.xpath.assert_called_once_with('.//td[@data-stat="lg_id"]')

    def test_league_abbreviation_is_first_abbreviation_text_content_when_matching_league_abbreviations(self):
        first_abbreviation = MagicMock()
        first_abbreviation.text_content = MagicMock(return_value="first abbreviation")

        second_abbreviation = MagicMock()
        second_abbreviation.text_content = MagicMock(return_value="second abbreviation")

        html = MagicMock()
        html.xpath = MagicMock(return_value=[first_abbreviation, second_abbreviation])

        self.assertEqual(
            PlayerPageTotalsRow(html=html).league_abbreviation,
            "first abbreviation"
        )
        html.xpath.assert_called_once_with('.//td[@data-stat="lg_id"]')

    def test_different_class_is_not_equal(self):
        self.assertNotEqual(
            PlayerPageTotalsRow(html=MagicMock()),
            "jaebaebae"
        )

    def test_different_html_but_same_class_is_not_equal(self):
        self.assertNotEqual(
            PlayerPageTotalsRow(html=MagicMock()),
            PlayerPageTotalsRow(html=MagicMock())
        )

    def test_same_html_and_same_class_is_equal(self):
        html = MagicMock()
        self.assertEqual(
            PlayerPageTotalsRow(html=html),
            PlayerPageTotalsRow(html=html),
        )


