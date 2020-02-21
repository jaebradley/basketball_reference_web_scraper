from unittest import TestCase
from unittest.mock import MagicMock

from basketball_reference_web_scraper.html import BasicBoxScoreRow


class TestBasicBoxScoreRow(TestCase):
    def setUp(self):
        self.html = MagicMock()

    def test_playing_time_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some playing time"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(BasicBoxScoreRow(html=self.html).playing_time, "some playing time")
        self.html.xpath.assert_called_once_with('td[@data-stat="mp"]')

    def test_playing_time_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(BasicBoxScoreRow(html=self.html).playing_time, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="mp"]')

    def test_minutes_played_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some minutes played"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(BasicBoxScoreRow(html=self.html).minutes_played, "some minutes played")
        self.html.xpath.assert_called_once_with('td[@data-stat="mp"]')

    def test_minutes_played_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(BasicBoxScoreRow(html=self.html).minutes_played, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="mp"]')

    def test_made_field_goals_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some made field goals"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(BasicBoxScoreRow(html=self.html).made_field_goals, "some made field goals")
        self.html.xpath.assert_called_once_with('td[@data-stat="fg"]')

    def test_made_field_goals_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(BasicBoxScoreRow(html=self.html).made_field_goals, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="fg"]')

    def test_attempted_field_goals_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some attempted field goals"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(BasicBoxScoreRow(html=self.html).attempted_field_goals, "some attempted field goals")
        self.html.xpath.assert_called_once_with('td[@data-stat="fga"]')

    def test_attempted_field_goals_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(BasicBoxScoreRow(html=self.html).attempted_field_goals, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="fga"]')

    def test_made_three_point_field_goals_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some made three point field goals"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(
            BasicBoxScoreRow(html=self.html).made_three_point_field_goals,
            "some made three point field goals",
        )
        self.html.xpath.assert_called_once_with('td[@data-stat="fg3"]')

    def test_made_three_point_field_goals_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(BasicBoxScoreRow(html=self.html).made_three_point_field_goals, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="fg3"]')

    def test_attempted_three_point_field_goals_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some attempted three point field goals"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(
            BasicBoxScoreRow(html=self.html).attempted_three_point_field_goals,
            "some attempted three point field goals",
        )
        self.html.xpath.assert_called_once_with('td[@data-stat="fg3a"]')

    def test_attempted_three_point_field_goals_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(BasicBoxScoreRow(html=self.html).attempted_three_point_field_goals, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="fg3a"]')

    def test_made_free_throws_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some made free throws"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(BasicBoxScoreRow(html=self.html).made_free_throws, "some made free throws")
        self.html.xpath.assert_called_once_with('td[@data-stat="ft"]')

    def test_made_free_throws_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(BasicBoxScoreRow(html=self.html).made_free_throws, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="ft"]')

    def test_attempted_free_throws_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some attempted free throws"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(BasicBoxScoreRow(html=self.html).attempted_free_throws, "some attempted free throws")
        self.html.xpath.assert_called_once_with('td[@data-stat="fta"]')

    def test_attempted_free_throws_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(BasicBoxScoreRow(html=self.html).attempted_free_throws, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="fta"]')

    def test_offensive_rebounds_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some offensive rebounds"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(BasicBoxScoreRow(html=self.html).offensive_rebounds, "some offensive rebounds")
        self.html.xpath.assert_called_once_with('td[@data-stat="orb"]')

    def test_offensive_rebounds_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(BasicBoxScoreRow(html=self.html).offensive_rebounds, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="orb"]')

    def test_defensive_rebounds_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some defensive rebounds"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(BasicBoxScoreRow(html=self.html).defensive_rebounds, "some defensive rebounds")
        self.html.xpath.assert_called_once_with('td[@data-stat="drb"]')

    def test_defensive_rebounds_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(BasicBoxScoreRow(html=self.html).defensive_rebounds, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="drb"]')

    def test_assists_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some assists"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(BasicBoxScoreRow(html=self.html).assists, "some assists")
        self.html.xpath.assert_called_once_with('td[@data-stat="ast"]')

    def test_assists_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(BasicBoxScoreRow(html=self.html).assists, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="ast"]')

    def test_steals(self):
        cell = MagicMock(text_content=MagicMock(return_value="some steals"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(BasicBoxScoreRow(html=self.html).steals, "some steals")
        self.html.xpath.assert_called_once_with('td[@data-stat="stl"]')

    def test_steals_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(BasicBoxScoreRow(html=self.html).steals, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="stl"]')

    def test_blocks_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some blocks"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(BasicBoxScoreRow(html=self.html).blocks, "some blocks")
        self.html.xpath.assert_called_once_with('td[@data-stat="blk"]')

    def test_blocks_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(BasicBoxScoreRow(html=self.html).blocks, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="blk"]')

    def test_turnovers_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some turnovers"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(BasicBoxScoreRow(html=self.html).turnovers, "some turnovers")
        self.html.xpath.assert_called_once_with('td[@data-stat="tov"]')

    def test_turnovers_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(BasicBoxScoreRow(html=self.html).turnovers, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="tov"]')

    def test_personal_fouls_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some personal fouls"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(BasicBoxScoreRow(html=self.html).personal_fouls, "some personal fouls")
        self.html.xpath.assert_called_once_with('td[@data-stat="pf"]')

    def test_personal_fouls_is_empty_string_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(BasicBoxScoreRow(html=self.html).personal_fouls, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="pf"]')

    def test_points(self):
        cell = MagicMock(text_content=MagicMock(return_value="some points"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(BasicBoxScoreRow(html=self.html).points, "some points")
        self.html.xpath.assert_called_once_with('td[@data-stat="pts"]')

    def test_points_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(BasicBoxScoreRow(html=self.html).points, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="pts"]')
