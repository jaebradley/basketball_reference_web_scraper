from unittest import TestCase
from unittest.mock import MagicMock

from basketball_reference_web_scraper.html import PlayerSeasonBoxScoresRow


class TestPlayerSeasonBoxScoresRow(TestCase):
    def test_not_equal_when_row_is_compared_against_non_row(self):
        self.assertNotEqual(1, PlayerSeasonBoxScoresRow(html=MagicMock()))

    def test_not_equal_when_both_rows_but_different_html(self):
        self.assertNotEqual(
            PlayerSeasonBoxScoresRow(html=MagicMock(name="first html")),
            PlayerSeasonBoxScoresRow(html=MagicMock(name="second html")),
        )

    def test_equal_when_both_rows_and_same_html(self):
        html = MagicMock(name="shared html")
        self.assertEqual(
            PlayerSeasonBoxScoresRow(html=html),
            PlayerSeasonBoxScoresRow(html=html),
        )
