from unittest import TestCase
from unittest.mock import MagicMock

from basketball_reference_web_scraper.html import PlayerSeasonBoxScoresTable


class TestPlayerSeasonBoxScoresTable(TestCase):
    def setUp(self):
        self.html = MagicMock()

    def test_rows_query_raises_not_implemented_error(self):
        table = PlayerSeasonBoxScoresTable(html=self.html)
        self.assertRaises(
            NotImplementedError,
            lambda: table.rows_query,
        )

    def test_rows_raises_not_implemented_error_when_rows_query_is_not_overridden(self):
        table = PlayerSeasonBoxScoresTable(html=self.html)
        self.assertRaises(
            NotImplementedError,
            lambda: table.rows,
        )

