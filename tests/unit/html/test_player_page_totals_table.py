from unittest import TestCase
from unittest.mock import MagicMock

from basketball_reference_web_scraper.html import PlayerPageTotalsTable, PlayerPageTotalsRow


class TestPlayerPageTotalsTable(TestCase):
    def test_rows_are_empty_array_when_no_results(self):
        html = MagicMock()
        html.xpath = MagicMock(return_value=[])

        self.assertEqual(
            PlayerPageTotalsTable(html=html).rows,
            []
        )
        html.xpath.assert_called_once_with('.//tbody/tr')

    def test_rows_when_results(self):
        first_row = MagicMock(name="first row html")
        second_row = MagicMock(name="second row html")

        html = MagicMock()
        html.xpath = MagicMock(return_value=[first_row, second_row])

        self.assertEqual(
            PlayerPageTotalsTable(html=html).rows,
            [
                PlayerPageTotalsRow(html=first_row),
                PlayerPageTotalsRow(html=second_row),
            ]
        )
        html.xpath.assert_called_once_with('.//tbody/tr')

    def test_different_class_is_not_equal(self):
        self.assertNotEqual(
            PlayerPageTotalsTable(html=MagicMock()),
            "jaebaebae"
        )

    def test_different_html_but_same_class_is_not_equal(self):
        self.assertNotEqual(
            PlayerPageTotalsTable(html=MagicMock()),
            PlayerPageTotalsTable(html=MagicMock())
        )

    def test_same_html_and_same_class_is_equal(self):
        html = MagicMock()
        self.assertEqual(
            PlayerPageTotalsTable(html=html),
            PlayerPageTotalsTable(html=html),
        )
