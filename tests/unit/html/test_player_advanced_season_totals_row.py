from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from basketball_reference_web_scraper.html import PlayerAdvancedSeasonTotalsRow


class TestPlayerAdvancedSeasonTotalsRow(TestCase):
    def setUp(self):
        self.html = MagicMock()

    def test_position_abbreviations_when_cells_exist(self):
        position_abbreviations = MagicMock()
        text_content = 'some text content'
        position_abbreviations.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[position_abbreviations])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).position_abbreviations, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="pos"]')

    def test_position_abbreviations_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).position_abbreviations, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="pos"]')

    def test_age_when_cells_exist(self):
        age = MagicMock()
        text_content = 'some text content'
        age.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[age])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).age, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="age"]')

    def test_age_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).age, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="age"]')

    def test_team_abbreviation_when_cells_exist(self):
        team_abbreviation = MagicMock()
        text_content = 'some text content'
        team_abbreviation.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[team_abbreviation])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).team_abbreviation, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="team_id"]')

    def test_team_abbreviation_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).team_abbreviation, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="team_id"]')

    def test_games_played_when_cells_exist(self):
        games_played = MagicMock()
        text_content = 'some text content'
        games_played.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[games_played])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).games_played, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="g"]')

    def test_games_played_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).games_played, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="g"]')

    def test_minutes_played_when_cells_exist(self):
        minutes_played = MagicMock()
        text_content = 'some text content'
        minutes_played.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[minutes_played])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).minutes_played, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="mp"]')

    def test_minutes_played_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).minutes_played, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="mp"]')

    def test_player_efficiency_rating_when_cells_exist(self):
        player_efficiency_rating = MagicMock()
        text_content = 'some text content'
        player_efficiency_rating.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[player_efficiency_rating])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).player_efficiency_rating, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="per"]')

    def test_player_efficiency_rating_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).player_efficiency_rating, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="per"]')

    def test_true_shooting_percentage_when_cells_exist(self):
        true_shooting_percentage = MagicMock()
        text_content = 'some text content'
        true_shooting_percentage.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[true_shooting_percentage])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).true_shooting_percentage, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="ts_pct"]')

    def test_true_shooting_percentage_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).true_shooting_percentage, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="ts_pct"]')

    def test_three_point_attempt_rate_when_cells_exist(self):
        three_point_attempt_rate = MagicMock()
        text_content = 'some text content'
        three_point_attempt_rate.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[three_point_attempt_rate])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).three_point_attempt_rate, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="fg3a_per_fga_pct"]')

    def test_three_point_attempt_rate_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).three_point_attempt_rate, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="fg3a_per_fga_pct"]')

    def test_free_throw_attempt_rate_when_cells_exist(self):
        free_throw_attempt_rate = MagicMock()
        text_content = 'some text content'
        free_throw_attempt_rate.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[free_throw_attempt_rate])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).free_throw_attempt_rate, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="fta_per_fga_pct"]')

    def test_free_throw_attempt_rate_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).free_throw_attempt_rate, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="fta_per_fga_pct"]')

    def test_offensive_rebound_percentage_when_cells_exist(self):
        offensive_rebound_percentage = MagicMock()
        text_content = 'some text content'
        offensive_rebound_percentage.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[offensive_rebound_percentage])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).offensive_rebound_percentage, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="orb_pct"]')

    def test_offensive_rebound_percentage_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).offensive_rebound_percentage, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="orb_pct"]')

    def test_defensive_rebound_percentage_when_cells_exist(self):
        defensive_rebound_percentage = MagicMock()
        text_content = 'some text content'
        defensive_rebound_percentage.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[defensive_rebound_percentage])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).defensive_rebound_percentage, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="drb_pct"]')

    def test_defensive_rebound_percentage_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).defensive_rebound_percentage, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="drb_pct"]')

    def test_total_rebound_percentage_when_cells_exist(self):
        total_rebound_percentage = MagicMock()
        text_content = 'some text content'
        total_rebound_percentage.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[total_rebound_percentage])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).total_rebound_percentage, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="trb_pct"]')

    def test_total_rebound_percentage_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).total_rebound_percentage, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="trb_pct"]')

    def test_assist_percentage_when_cells_exist(self):
        assist_percentage = MagicMock()
        text_content = 'some text content'
        assist_percentage.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[assist_percentage])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).assist_percentage, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="ast_pct"]')

    def test_assist_percentage_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).assist_percentage, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="ast_pct"]')

    def test_steal_percentage_when_cells_exist(self):
        steal_percentage = MagicMock()
        text_content = 'some text content'
        steal_percentage.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[steal_percentage])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).steal_percentage, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="stl_pct"]')

    def test_steal_percentage_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).steal_percentage, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="stl_pct"]')

    def test_block_percentage_when_cells_exist(self):
        block_percentage = MagicMock()
        text_content = 'some text content'
        block_percentage.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[block_percentage])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).block_percentage, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="blk_pct"]')

    def test_block_percentage_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).block_percentage, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="blk_pct"]')

    def test_turnover_percentage_when_cells_exist(self):
        turnover_percentage = MagicMock()
        text_content = 'some text content'
        turnover_percentage.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[turnover_percentage])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).turnover_percentage, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="tov_pct"]')

    def test_turnover_percentage_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).turnover_percentage, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="tov_pct"]')

    def test_usage_percentage_when_cells_exist(self):
        usage_percentage = MagicMock()
        text_content = 'some text content'
        usage_percentage.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[usage_percentage])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).usage_percentage, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="usg_pct"]')

    def test_usage_percentage_is_empty_string_when_no_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).usage_percentage, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="usg_pct"]')

    def test_offensive_win_shares_when_cells_exist(self):
        offensive_win_shares = MagicMock()
        text_content = 'some text content'
        offensive_win_shares.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[offensive_win_shares])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).offensive_win_shares, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="ows"]')

    def test_offensive_win_shares_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).offensive_win_shares, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="ows"]')

    def test_defensive_win_shares_when_cells_exist(self):
        defensive_win_shares = MagicMock()
        text_content = 'some text content'
        defensive_win_shares.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[defensive_win_shares])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).defensive_win_shares, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="dws"]')

    def test_defensive_win_shares_is_empty_string_when_no_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).defensive_win_shares, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="dws"]')

    def test_win_shares_when_cells_exist(self):
        win_shares = MagicMock()
        text_content = 'some text content'
        win_shares.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[win_shares])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).win_shares, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="ws"]')

    def test_win_shares_is_empty_string_when_no_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).win_shares, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="ws"]')

    def test_win_shares_per_48_minutes_when_cells_exist(self):
        win_shares_per_48_minutes = MagicMock()
        text_content = 'some text content'
        win_shares_per_48_minutes.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[win_shares_per_48_minutes])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).win_shares_per_48_minutes, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="ws_per_48"]')

    def test_win_shares_per_48_minutes_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).win_shares_per_48_minutes, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="ws_per_48"]')

    def test_offensive_plus_minus_when_cells_exist(self):
        offensive_plus_minus = MagicMock()
        text_content = 'some text content'
        offensive_plus_minus.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[offensive_plus_minus])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).offensive_plus_minus, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="obpm"]')

    def test_offensive_plus_minus_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).offensive_plus_minus, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="obpm"]')

    def test_defensive_plus_minus_when_cells_exist(self):
        defensive_plus_minus = MagicMock()
        text_content = 'some text content'
        defensive_plus_minus.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[defensive_plus_minus])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).defensive_plus_minus, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="dbpm"]')

    def test_defensive_plus_minus_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).defensive_plus_minus, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="dbpm"]')

    def test_plus_minus_when_cells_exist(self):
        plus_minus = MagicMock()
        text_content = 'some text content'
        plus_minus.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[plus_minus])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).plus_minus, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="bpm"]')

    def test_plus_minus_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).plus_minus, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="bpm"]')

    def test_value_over_replacement_player_when_cells_exist(self):
        value_over_replacement_player = MagicMock()
        text_content = 'some text content'
        value_over_replacement_player.text_content = MagicMock(return_value=text_content)
        self.html.xpath = MagicMock(return_value=[value_over_replacement_player])

        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).value_over_replacement_player, text_content)
        self.html.xpath.assert_called_once_with('td[@data-stat="vorp"]')

    def test_value_over_replacement_player_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerAdvancedSeasonTotalsRow(html=self.html).value_over_replacement_player, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="vorp"]')

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
