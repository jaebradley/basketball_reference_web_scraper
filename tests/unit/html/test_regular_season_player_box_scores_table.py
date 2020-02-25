from unittest import TestCase
from unittest.mock import MagicMock

from basketball_reference_web_scraper.html import RegularSeasonPlayerBoxScoresTable, PlayerSeasonBoxScoresRow


class TestRegularSeasonPlayerBoxScoresTable(TestCase):
    def setUp(self):
        self.html = MagicMock()

    def test_rows_query(self):
        self.assertEqual(
            '//tbody/tr[not(contains(@class, "thead"))]',
            RegularSeasonPlayerBoxScoresTable(html=self.html).rows_query,
        )

    def test_rows_returns_empty_array_when_there_are_not_any_matching_rows(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertListEqual([], RegularSeasonPlayerBoxScoresTable(html=self.html).rows)

    def test_rows_returns_populated_array_when_there_are_matching_rows(self):
        first_row_html = MagicMock(name="first matching row html")
        second_row_html = MagicMock(name="second matching row html")
        self.html.xpath = MagicMock(return_value=[first_row_html, second_row_html])
        self.assertListEqual([
                PlayerSeasonBoxScoresRow(html=first_row_html),
                PlayerSeasonBoxScoresRow(html=second_row_html),
            ],
            RegularSeasonPlayerBoxScoresTable(html=self.html).rows,
        )
