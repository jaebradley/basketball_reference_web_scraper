from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from basketball_reference_web_scraper.html import PlayerSeasonTotalsRow


class TestPlayerSeasonTotalsRow(TestCase):
    def setUp(self):
        self.html = MagicMock()

    def test_player_name_cell(self):
        player_name_cell = MagicMock()
        self.html.__getitem__ = MagicMock(return_value=player_name_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).player_name_cell, player_name_cell)
        self.html.__getitem__.assert_called_once_with(1)

    @patch.object(PlayerSeasonTotalsRow, 'player_name_cell', new_callable=PropertyMock)
    def test_slug(self, mock_player_name_cell):
        player_name_cell = MagicMock()
        mock_player_name_cell.return_value = player_name_cell

        slug = "some slug"
        player_name_cell.get = MagicMock(return_value=slug)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).slug, slug)
        mock_player_name_cell.assert_called_once_with()
        player_name_cell.get.assert_called_once_with('data-append-csv')

    @patch.object(PlayerSeasonTotalsRow, 'player_name_cell', new_callable=PropertyMock)
    def test_name(self, mock_player_name_cell):
        player_name_cell = MagicMock()
        mock_player_name_cell.return_value = player_name_cell

        name = "jaebaebae"
        player_name_cell.text_content = MagicMock(return_value=name)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).name, name)
        mock_player_name_cell.assert_called_once_with()
        player_name_cell.text_content.assert_called_once_with()

    def test_position_abbreviations(self):
        abbreviations = "some abbreviations"
        abbreviations_cell = MagicMock()
        abbreviations_cell.text_content = MagicMock(return_value=abbreviations)
        self.html.__getitem__ = MagicMock(return_value=abbreviations_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).position_abbreviations, abbreviations)
        self.html.__getitem__.assert_called_once_with(2)
        abbreviations_cell.text_content.assert_called_once_with()

    def test_age(self):
        age = "some age"
        age_cell = MagicMock()
        age_cell.text_content = MagicMock(return_value=age)
        self.html.__getitem__ = MagicMock(return_value=age_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).age, age)
        self.html.__getitem__.assert_called_once_with(3)
        age_cell.text_content.assert_called_once_with()

    def test_team_abbreviation(self):
        team_abbreviation = "some team abbreviation"
        team_abbreviation_cell = MagicMock()
        team_abbreviation_cell.text_content = MagicMock(return_value=team_abbreviation)
        self.html.__getitem__ = MagicMock(return_value=team_abbreviation_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).team_abbreviation, team_abbreviation)
        self.html.__getitem__.assert_called_once_with(4)
        team_abbreviation_cell.text_content.assert_called_once_with()

    def test_games_played(self):
        games_played = "some number of games played"
        games_played_cell = MagicMock()
        games_played_cell.text_content = MagicMock(return_value=games_played)
        self.html.__getitem__ = MagicMock(return_value=games_played_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).games_played, games_played)
        self.html.__getitem__.assert_called_once_with(5)
        games_played_cell.text_content.asset_called_once_with()

    def test_games_started(self):
        games_started = "some number of games started"
        games_started_cell = MagicMock()
        games_started_cell.text_content = MagicMock(return_value=games_started)
        self.html.__getitem__ = MagicMock(return_value=games_started_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).games_started, games_started)
        self.html.__getitem__.assert_called_once_with(6)
        games_started_cell.text_content.assert_called_once_with()

    def test_minutes_played(self):
        minutes_played = "some number of minutes played"
        minutes_played_cell = MagicMock()
        minutes_played_cell.text_content = MagicMock(return_value=minutes_played)
        self.html.__getitem__ = MagicMock(return_value=minutes_played_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).minutes_played, minutes_played)
        self.html.__getitem__.assert_called_once_with(7)
        minutes_played_cell.text_content.asset_called_once_with()

    def test_made_field_goals(self):
        made_field_goals = "some made field goals"
        made_field_goals_cell = MagicMock()
        made_field_goals_cell.text_content = MagicMock(return_value=made_field_goals)
        self.html.__getitem__ = MagicMock(return_value=made_field_goals_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).made_field_goals, made_field_goals)
        self.html.__getitem__.assert_called_once_with(8)
        made_field_goals_cell.text_content.assert_called_once_with()

    def test_attempted_field_goals(self):
        attempted_field_goals = "some attempted field goals"
        attempted_field_goals_cell = MagicMock()
        attempted_field_goals_cell.text_content = MagicMock(return_value=attempted_field_goals)
        self.html.__getitem__ = MagicMock(return_value=attempted_field_goals_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).attempted_field_goals, attempted_field_goals)
        self.html.__getitem__.assert_called_once_with(9)
        attempted_field_goals_cell.text_content.assert_called_once_with()

    def test_made_three_point_field_goals(self):
        made_three_point_field_goals = "some made three point field goals"
        made_three_point_field_goals_cell = MagicMock()
        made_three_point_field_goals_cell.text_content = MagicMock(return_value=made_three_point_field_goals)
        self.html.__getitem__ = MagicMock(return_value=made_three_point_field_goals_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).made_three_point_field_goals, made_three_point_field_goals)
        self.html.__getitem__.assert_called_once_with(11)
        made_three_point_field_goals_cell.text_content.assert_called_once_with()

    def test_attempted_three_point_field_goals(self):
        attempted_three_point_field_goals = "some attempted three point field goals"
        attempted_three_point_field_goals_cell = MagicMock()
        attempted_three_point_field_goals_cell.text_content = MagicMock(return_value=attempted_three_point_field_goals)
        self.html.__getitem__ = MagicMock(return_value=attempted_three_point_field_goals_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).attempted_three_point_field_goals, attempted_three_point_field_goals)
        self.html.__getitem__.assert_called_once_with(12)
        attempted_three_point_field_goals_cell.text_content.assert_called_once_with()

    def test_made_free_throws(self):
        made_free_throws = "some made free throws"
        made_free_throws_cell = MagicMock()
        made_free_throws_cell.text_content = MagicMock(return_value=made_free_throws)
        self.html.__getitem__ = MagicMock(return_value=made_free_throws_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).made_free_throws, made_free_throws)
        self.html.__getitem__.assert_called_once_with(18)
        made_free_throws_cell.text_content.assert_called_once_with()

    def test_attempted_free_throws(self):
        attempted_free_throws = "some attempted free throws"
        attempted_free_throws_cell = MagicMock()
        attempted_free_throws_cell.text_content = MagicMock(return_value=attempted_free_throws)
        self.html.__getitem__ = MagicMock(return_value=attempted_free_throws_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).attempted_free_throws, attempted_free_throws)
        self.html.__getitem__.assert_called_once_with(19)
        attempted_free_throws_cell.text_content.assert_called_once_with()

    def test_offensive_rebounds(self):
        offensive_rebounds = "some offensive rebounds"
        offensive_rebounds_cell = MagicMock()
        offensive_rebounds_cell.text_content = MagicMock(return_value=offensive_rebounds)
        self.html.__getitem__ = MagicMock(return_value=offensive_rebounds_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).offensive_rebounds, offensive_rebounds)
        self.html.__getitem__.assert_called_once_with(21)
        offensive_rebounds_cell.text_content.assert_called_once_with()

    def test_defensive_rebounds(self):
        defensive_rebounds = "some defensive rebounds"
        defensive_rebounds_cell = MagicMock()
        defensive_rebounds_cell.text_content = MagicMock(return_value=defensive_rebounds)
        self.html.__getitem__ = MagicMock(return_value=defensive_rebounds_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).defensive_rebounds, defensive_rebounds)
        self.html.__getitem__.assert_called_once_with(22)
        defensive_rebounds_cell.text_content.assert_called_once_with()

    def test_assists(self):
        assists = "some assists"
        assists_cell = MagicMock()
        assists_cell.text_content = MagicMock(return_value=assists)
        self.html.__getitem__ = MagicMock(return_value=assists_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).assists, assists)
        self.html.__getitem__.assert_called_once_with(24)
        assists_cell.text_content.assert_called_once_with()

    def test_steals(self):
        steals = "some steals"
        steals_cell = MagicMock()
        steals_cell.text_content = MagicMock(return_value=steals)
        self.html.__getitem__ = MagicMock(return_value=steals_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).steals, steals)
        self.html.__getitem__.assert_called_once_with(25)
        steals_cell.text_content.assert_called_once_with()

    def test_blocks(self):
        blocks = "some blocks"
        blocks_cell = MagicMock()
        blocks_cell.text_content = MagicMock(return_value=blocks)
        self.html.__getitem__ = MagicMock(return_value=blocks_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).blocks, blocks)
        self.html.__getitem__.assert_called_once_with(26)
        blocks_cell.text_content.assert_called_once_with()

    def test_turnovers(self):
        turnovers = "some turnovers"
        turnovers_cell = MagicMock()
        turnovers_cell.text_content = MagicMock(return_value=turnovers)
        self.html.__getitem__ = MagicMock(return_value=turnovers_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).turnovers, turnovers)
        self.html.__getitem__.assert_called_once_with(27)
        turnovers_cell.text_content.assert_called_once_with()

    def test_personal_fouls(self):
        personal_fouls = "some personal fouls"
        personal_fouls_cell = MagicMock()
        personal_fouls_cell.text_content = MagicMock(return_value=personal_fouls)
        self.html.__getitem__ = MagicMock(return_value=personal_fouls_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).personal_fouls, personal_fouls)
        self.html.__getitem__.assert_called_once_with(28)
        personal_fouls_cell.text_content.assert_called_once_with()

    def test_points(self):
        points = "some points"
        points_cell = MagicMock()
        points_cell.text_content = MagicMock(return_value=points)
        self.html.__getitem__ = MagicMock(return_value=points_cell)

        self.assertEqual(PlayerSeasonTotalsRow(html=self.html).points, points)
        self.html.__getitem__.assert_called_once_with(29)
        points_cell.text_content.assert_called_once_with()

    @patch.object(PlayerSeasonTotalsRow, 'team_abbreviation', new_callable=PropertyMock)
    def test_is_combined_totals_when_team_abbreviation_is_tot(self, mocked_team_abbreviation):
        mocked_team_abbreviation.return_value = "TOT"
        self.assertTrue(PlayerSeasonTotalsRow(html=self.html).is_combined_totals)

    @patch.object(PlayerSeasonTotalsRow, 'team_abbreviation', new_callable=PropertyMock)
    def test_is_not_combined_totals_when_team_abbreviation_is_tot(self, mocked_team_abbreviation):
        mocked_team_abbreviation.return_value = "jaebaebae"
        self.assertFalse(PlayerSeasonTotalsRow(html=self.html).is_combined_totals)
