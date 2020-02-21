from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from basketball_reference_web_scraper.html import PlayerSeasonTotalsRow


class TestPlayerSeasonTotalsRow(TestCase):
    def setUp(self):
        self.html = MagicMock()

    def test_position_abbreviations_when_cells_exist(self):
        self.html.xpath = MagicMock(
            return_value=[
                MagicMock(text_content=MagicMock(return_value="some position abbreviations"))
            ]
        )

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).position_abbreviations, "some position abbreviations")
        self.html.xpath.assert_called_once_with('td[@data-stat="pos"]')

    def test_position_abbreviations_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).position_abbreviations, "")
        self.html.xpath.assert_called_once_with('td[@data-stat="pos"]')

    def test_age_when_cells_exist(self):
        self.html.xpath = MagicMock(
            return_value=[
                MagicMock(text_content=MagicMock(return_value="some age"))
            ]
        )

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).age, "some age")
        self.html.xpath.assert_called_once_with('td[@data-stat="age"]')

    def test_age_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).age, "")
        self.html.xpath.assert_called_once_with('td[@data-stat="age"]')

    def test_games_played_when_cells_exist(self):
        self.html.xpath = MagicMock(
            return_value=[
                MagicMock(text_content=MagicMock(return_value="some games played"))
            ]
        )

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).games_played, "some games played")
        self.html.xpath.assert_called_once_with('td[@data-stat="g"]')

    def test_games_played_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).games_played, "")
        self.html.xpath.assert_called_once_with('td[@data-stat="g"]')

    def test_games_started_when_cells_exist(self):
        self.html.xpath = MagicMock(
            return_value=[
                MagicMock(text_content=MagicMock(return_value="some games started"))
            ]
        )

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).games_started, "some games started")
        self.html.xpath.assert_called_once_with('td[@data-stat="gs"]')

    def test_games_started_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).games_started, "")
        self.html.xpath.assert_called_once_with('td[@data-stat="gs"]')

    @patch.object(PlayerSeasonTotalsRow, 'team_abbreviation', new_callable=PropertyMock)
    def test_is_combined_totals_when_team_abbreviation_is_tot(self, mocked_team_abbreviation):
        mocked_team_abbreviation.return_value = "TOT"
        self.assertTrue(PlayerSeasonTotalsRow(html=self.html).is_combined_totals)

    @patch.object(PlayerSeasonTotalsRow, 'team_abbreviation', new_callable=PropertyMock)
    def test_is_not_combined_totals_when_team_abbreviation_is_tot(self, mocked_team_abbreviation):
        mocked_team_abbreviation.return_value = "jaebaebae"
        self.assertFalse(PlayerSeasonTotalsRow(html=self.html).is_combined_totals)
