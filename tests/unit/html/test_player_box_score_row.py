from unittest import TestCase
from unittest.mock import MagicMock

from basketball_reference_web_scraper.html import PlayerBoxScoreRow


class TestPlayerBoxScoreRow(TestCase):
    def setUp(self):
        self.html = MagicMock()

    def test_not_equal_when_row_is_compared_against_non_row(self):
        self.assertNotEqual(1, PlayerBoxScoreRow(html=MagicMock()))

    def test_not_equal_when_both_rows_but_different_html(self):
        self.assertNotEqual(
            PlayerBoxScoreRow(html=MagicMock(name="first html")),
            PlayerBoxScoreRow(html=MagicMock(name="second html")),
        )

    def test_equal_when_both_rows_and_same_html(self):
        html = MagicMock(name="shared html")
        self.assertEqual(
            PlayerBoxScoreRow(html=html),
            PlayerBoxScoreRow(html=html),
        )

    def test_team_abbreviation_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some team abbreviation"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).team_abbreviation, "some team abbreviation")
        self.html.xpath.assert_called_once_with('td[@data-stat="team_id"]')

    def test_team_abbreviation_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).team_abbreviation, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="team_id"]')

    def test_location_abbreviation_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some location abbreviation"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).location_abbreviation, "some location abbreviation")
        self.html.xpath.assert_called_once_with('td[@data-stat="game_location"]')

    def test_location_abbreviation_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).location_abbreviation, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="game_location"]')

    def test_opponent_abbreviation_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some opponent abbreviation"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).opponent_abbreviation, "some opponent abbreviation")
        self.html.xpath.assert_called_once_with('td[@data-stat="opp_id"]')

    def test_opponent_abbreviation_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).opponent_abbreviation, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="opp_id"]')

    def test_outcome_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some outcome"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).outcome, "some outcome")
        self.html.xpath.assert_called_once_with('td[@data-stat="game_result"]')

    def test_outcome_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).outcome, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="game_result"]')

    def test_plus_minus_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some plus minus"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).plus_minus, "some plus minus")
        self.html.xpath.assert_called_once_with('td[@data-stat="plus_minus"]')

    def test_plus_minus_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).plus_minus, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="plus_minus"]')

    def test_game_score_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some game score"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).game_score, "some game score")
        self.html.xpath.assert_called_once_with('td[@data-stat="game_score"]')

    def test_game_score_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).game_score, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="game_score"]')

