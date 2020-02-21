from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from basketball_reference_web_scraper.html import PlayerGameBoxScoreRow


class TestPlayerGameBoxScoreRow(TestCase):
    def setUp(self):
        self.html = MagicMock()

    def test_player_cell_when_cells_exist(self):
        cell = MagicMock()
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerGameBoxScoreRow(html=self.html).player_cell, cell)
        self.html.xpath.assert_called_once_with('td[@data-stat="player"]')

    def test_player_cell_is_none_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertIsNone(PlayerGameBoxScoreRow(html=self.html).player_cell)
        self.html.xpath.assert_called_once_with('td[@data-stat="player"]')

    @patch.object(PlayerGameBoxScoreRow, 'player_cell', new_callable=PropertyMock)
    def test_slug_when_player_cell_is_not_none(self, mocked_player_cell):
        cell = MagicMock(get=MagicMock(return_value="some slug"))
        mocked_player_cell.return_value = cell
        self.assertEqual(PlayerGameBoxScoreRow(html=self.html).slug, "some slug")
        cell.get.assert_called_once_with('data-append-csv')

    @patch.object(PlayerGameBoxScoreRow, 'player_cell', new_callable=PropertyMock)
    def test_slug_when_player_cell_is_none(self, mocked_player_cell):
        mocked_player_cell.return_value = None
        self.assertEqual(PlayerGameBoxScoreRow(html=self.html).slug, "")

    @patch.object(PlayerGameBoxScoreRow, 'player_cell', new_callable=PropertyMock)
    def test_name_when_player_cell_is_not_none(self, mocked_player_cell):
        cell = MagicMock(text_content=MagicMock(return_value="some name"))
        mocked_player_cell.return_value = cell
        self.assertEqual(PlayerGameBoxScoreRow(html=self.html).name, "some name")
        cell.text_content.assert_called_once_with()

    @patch.object(PlayerGameBoxScoreRow, 'player_cell', new_callable=PropertyMock)
    def test_name_when_player_cell_is_none(self, mocked_player_cell):
        mocked_player_cell.return_value = None
        self.assertEqual(PlayerGameBoxScoreRow(html=self.html).name, "")
