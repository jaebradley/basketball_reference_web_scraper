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

    def test_playing_time_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some playing time"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).playing_time, "some playing time")
        self.html.xpath.assert_called_once_with('td[@data-stat="mp"]')

    def test_playing_time_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).playing_time, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="mp"]')

    def test_made_field_goals_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some made field goals"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).made_field_goals, "some made field goals")
        self.html.xpath.assert_called_once_with('td[@data-stat="fg"]')

    def test_made_field_goals_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).made_field_goals, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="fg"]')

    def test_attempted_field_goals_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some attempted field goals"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).attempted_field_goals, "some attempted field goals")
        self.html.xpath.assert_called_once_with('td[@data-stat="fga"]')

    def test_attempted_field_goals_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).attempted_field_goals, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="fga"]')

    def test_made_three_point_field_goals_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some made three point field goals"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(
            PlayerBoxScoreRow(html=self.html).made_three_point_field_goals,
            "some made three point field goals",
        )
        self.html.xpath.assert_called_once_with('td[@data-stat="fg3"]')

    def test_made_three_point_field_goals_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).made_three_point_field_goals, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="fg3"]')

    def test_attempted_three_point_field_goals_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some attempted three point field goals"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(
            PlayerBoxScoreRow(html=self.html).attempted_three_point_field_goals,
            "some attempted three point field goals",
        )
        self.html.xpath.assert_called_once_with('td[@data-stat="fg3a"]')

    def test_attempted_three_point_field_goals_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).attempted_three_point_field_goals, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="fg3a"]')

    def test_made_free_throws_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some made free throws"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).made_free_throws, "some made free throws")
        self.html.xpath.assert_called_once_with('td[@data-stat="ft"]')

    def test_made_free_throws_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).made_free_throws, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="ft"]')

    def test_attempted_free_throws_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some attempted free throws"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).attempted_free_throws, "some attempted free throws")
        self.html.xpath.assert_called_once_with('td[@data-stat="fta"]')

    def test_attempted_free_throws_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).attempted_free_throws, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="fta"]')

    def test_offensive_rebounds_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some offensive rebounds"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).offensive_rebounds, "some offensive rebounds")
        self.html.xpath.assert_called_once_with('td[@data-stat="orb"]')

    def test_offensive_rebounds_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).offensive_rebounds, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="orb"]')

    def test_defensive_rebounds_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some defensive rebounds"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).defensive_rebounds, "some defensive rebounds")
        self.html.xpath.assert_called_once_with('td[@data-stat="drb"]')

    def test_defensive_rebounds_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).defensive_rebounds, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="drb"]')

    def test_assists_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some assists"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).assists, "some assists")
        self.html.xpath.assert_called_once_with('td[@data-stat="ast"]')

    def test_assists_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).assists, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="ast"]')

    def test_steals(self):
        cell = MagicMock(text_content=MagicMock(return_value="some steals"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).steals, "some steals")
        self.html.xpath.assert_called_once_with('td[@data-stat="stl"]')

    def test_steals_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).steals, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="stl"]')

    def test_blocks_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some blocks"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).blocks, "some blocks")
        self.html.xpath.assert_called_once_with('td[@data-stat="blk"]')

    def test_blocks_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).blocks, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="blk"]')

    def test_turnovers_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some turnovers"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).turnovers, "some turnovers")
        self.html.xpath.assert_called_once_with('td[@data-stat="tov"]')

    def test_turnovers_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).turnovers, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="tov"]')

    def test_personal_fouls_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some personal fouls"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).personal_fouls, "some personal fouls")
        self.html.xpath.assert_called_once_with('td[@data-stat="pf"]')

    def test_personal_fouls_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerBoxScoreRow(html=self.html).personal_fouls, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="pf"]')

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

