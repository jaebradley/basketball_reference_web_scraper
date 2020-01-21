from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from basketball_reference_web_scraper.html import PlayerAdvancedSeasonTotalsRow


class TestPlayerAdvancedSeasonTotalsRow(TestCase):
    def setUp(self):
        self.html = MagicMock()

    def test_player_name_cell(self):
        player_name_cell = MagicMock()
        self.html.__getitem__ = MagicMock(return_value=player_name_cell)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).player_name_cell, player_name_cell)
        self.html.__getitem__.assert_called_once_with(1)

    @patch.object(PlayerAdvancedSeasonTotalsRow, 'player_name_cell', new_callable=PropertyMock)
    def test_slug(self, mock_player_name_cell):
        player_name_cell = MagicMock()
        mock_player_name_cell.return_value = player_name_cell

        row = PlayerAdvancedSeasonTotalsRow(html=self.html)
        slug = "some slug"
        player_name_cell.get = MagicMock(return_value=slug)

        self.assertEqual(row.slug, slug)
        mock_player_name_cell.assert_called_once_with()
        player_name_cell.get.assert_called_once_with('data-append-csv')

    @patch.object(PlayerAdvancedSeasonTotalsRow, 'player_name_cell', new_callable=PropertyMock)
    def test_name(self, mock_player_name_cell):
        player_name_cell = MagicMock()
        mock_player_name_cell.return_value = player_name_cell

        name = "some name"
        player_name_cell.text_content = MagicMock(return_value=name)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).name, name)
        mock_player_name_cell.assert_called_once_with()
        player_name_cell.text_content.assert_called_once_with()

    def test_position_abbreviations(self):
        position_abbreviations = MagicMock()
        text_content = 'some text content'
        position_abbreviations.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=position_abbreviations)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).position_abbreviations, text_content)
        self.html.__getitem__.assert_called_once_with(2)

    def test_age(self):
        age = MagicMock()
        text_content = 'some text content'
        age.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=age)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).age, text_content)
        self.html.__getitem__.assert_called_once_with(3)

    def test_team_abbreviation(self):
        team_abbreviation = MagicMock()
        text_content = 'some text content'
        team_abbreviation.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=team_abbreviation)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).team_abbreviation, text_content)
        self.html.__getitem__.assert_called_once_with(4)

    def test_games_played(self):
        games_played = MagicMock()
        text_content = 'some text content'
        games_played.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=games_played)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).games_played, text_content)
        self.html.__getitem__.assert_called_once_with(5)

    def test_minutes_played(self):
        minutes_played = MagicMock()
        text_content = 'some text content'
        minutes_played.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=minutes_played)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).minutes_played, text_content)
        self.html.__getitem__.assert_called_once_with(6)

    def test_player_efficiency_rating(self):
        player_efficiency_rating = MagicMock()
        text_content = 'some text content'
        player_efficiency_rating.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=player_efficiency_rating)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).player_efficiency_rating, text_content)
        self.html.__getitem__.assert_called_once_with(7)

    def test_true_shooting_percentage(self):
        true_shooting_percentage = MagicMock()
        text_content = 'some text content'
        true_shooting_percentage.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=true_shooting_percentage)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).true_shooting_percentage, text_content)
        self.html.__getitem__.assert_called_once_with(8)

    def test_three_point_attempt_rate(self):
        three_point_attempt_rate = MagicMock()
        text_content = 'some text content'
        three_point_attempt_rate.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=three_point_attempt_rate)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).three_point_attempt_rate, text_content)
        self.html.__getitem__.assert_called_once_with(9)

    def test_free_throw_attempt_rate(self):
        free_throw_attempt_rate = MagicMock()
        text_content = 'some text content'
        free_throw_attempt_rate.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=free_throw_attempt_rate)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).free_throw_attempt_rate, text_content)
        self.html.__getitem__.assert_called_once_with(10)

    def test_offensive_rebound_percentage(self):
        offensive_rebound_percentage = MagicMock()
        text_content = 'some text content'
        offensive_rebound_percentage.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=offensive_rebound_percentage)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).offensive_rebound_percentage, text_content)
        self.html.__getitem__.assert_called_once_with(11)

    def test_defensive_rebound_percentage(self):
        defensive_rebound_percentage = MagicMock()
        text_content = 'some text content'
        defensive_rebound_percentage.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=defensive_rebound_percentage)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).defensive_rebound_percentage, text_content)
        self.html.__getitem__.assert_called_once_with(12)

    def test_total_rebound_percentage(self):
        total_rebound_percentage = MagicMock()
        text_content = 'some text content'
        total_rebound_percentage.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=total_rebound_percentage)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).total_rebound_percentage, text_content)
        self.html.__getitem__.assert_called_once_with(13)

    def test_assist_percentage(self):
        assist_percentage = MagicMock()
        text_content = 'some text content'
        assist_percentage.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=assist_percentage)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).assist_percentage, text_content)
        self.html.__getitem__.assert_called_once_with(14)

    def test_steal_percentage(self):
        steal_percentage = MagicMock()
        text_content = 'some text content'
        steal_percentage.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=steal_percentage)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).steal_percentage, text_content)
        self.html.__getitem__.assert_called_once_with(15)

    def test_block_percentage(self):
        block_percentage = MagicMock()
        text_content = 'some text content'
        block_percentage.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=block_percentage)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).block_percentage, text_content)
        self.html.__getitem__.assert_called_once_with(16)

    def test_turnover_percentage(self):
        turnover_percentage = MagicMock()
        text_content = 'some text content'
        turnover_percentage.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=turnover_percentage)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).turnover_percentage, text_content)
        self.html.__getitem__.assert_called_once_with(17)

    def test_usage_percentage(self):
        usage_percentage = MagicMock()
        text_content = 'some text content'
        usage_percentage.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=usage_percentage)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).usage_percentage, text_content)
        self.html.__getitem__.assert_called_once_with(18)

    def test_offensive_win_shares(self):
        offensive_win_shares = MagicMock()
        text_content = 'some text content'
        offensive_win_shares.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=offensive_win_shares)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).offensive_win_shares, text_content)
        self.html.__getitem__.assert_called_once_with(20)

    def test_defensive_win_shares(self):
        defensive_win_shares = MagicMock()
        text_content = 'some text content'
        defensive_win_shares.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=defensive_win_shares)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).defensive_win_shares, text_content)
        self.html.__getitem__.assert_called_once_with(21)

    def test_win_shares(self):
        win_shares = MagicMock()
        text_content = 'some text content'
        win_shares.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=win_shares)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).win_shares, text_content)
        self.html.__getitem__.assert_called_once_with(22)

    def test_win_shares_per_48_minutes(self):
        win_shares_per_48_minutes = MagicMock()
        text_content = 'some text content'
        win_shares_per_48_minutes.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=win_shares_per_48_minutes)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).win_shares_per_48_minutes, text_content)
        self.html.__getitem__.assert_called_once_with(23)

    def test_offensive_plus_minus(self):
        offensive_plus_minus = MagicMock()
        text_content = 'some text content'
        offensive_plus_minus.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=offensive_plus_minus)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).offensive_plus_minus, text_content)
        self.html.__getitem__.assert_called_once_with(25)

    def test_defensive_plus_minus(self):
        defensive_plus_minus = MagicMock()
        text_content = 'some text content'
        defensive_plus_minus.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=defensive_plus_minus)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).defensive_plus_minus, text_content)
        self.html.__getitem__.assert_called_once_with(26)

    def test_plus_minus(self):
        plus_minus = MagicMock()
        text_content = 'some text content'
        plus_minus.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=plus_minus)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).plus_minus, text_content)
        self.html.__getitem__.assert_called_once_with(27)

    def test_value_over_replacement_player(self):
        value_over_replacement_player = MagicMock()
        text_content = 'some text content'
        value_over_replacement_player.text_content = MagicMock(return_value=text_content)
        self.html.__getitem__ = MagicMock(return_value=value_over_replacement_player)

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).value_over_replacement_player, text_content)
        self.html.__getitem__.assert_called_once_with(28)

    @patch.object(
        PlayerAdvancedSeasonTotalsRow,
        'team_abbreviation',
        new_callable=PropertyMock,
        return_value='Not Total'
    )
    def test_is_not_combined_totals_when_team_abbreviation_is_not_TOT(self, _):
        self.assertFalse(PlayerAdvancedSeasonTotalsRow(html=self.html).is_combined_totals)

    @patch.object(
        PlayerAdvancedSeasonTotalsRow,
        'team_abbreviation',
        new_callable=PropertyMock,
        return_value='TOT'
    )
    def test_is_combined_totals_when_team_abbreviation_is_TOT(self, _):
        self.assertTrue(PlayerAdvancedSeasonTotalsRow(html=self.html).is_combined_totals)
