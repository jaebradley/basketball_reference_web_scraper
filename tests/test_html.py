from unittest import TestCase
from unittest.mock import MagicMock

from basketball_reference_web_scraper.html import TeamTotalRow


class TestTeamTotalRow(TestCase):
    def setUp(self):
        self.html = MagicMock()

    def test_minutes_played_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some minutes played"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(TeamTotalRow(html=self.html).minutes_played, "some minutes played")

    def test_minutes_played_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(TeamTotalRow(html=self.html).minutes_played, '')

    def test_made_field_goals_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some made field goals"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(TeamTotalRow(html=self.html).made_field_goals, "some made field goals")

    def test_made_field_goals_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(TeamTotalRow(html=self.html).made_field_goals, '')

    def test_attempted_field_goals_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some attempted field goals"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(TeamTotalRow(html=self.html).attempted_field_goals, "some attempted field goals")

    def test_attempted_field_goals_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(TeamTotalRow(html=self.html).attempted_field_goals, '')

    def test_made_three_point_field_goals_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some made three point field goals"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(TeamTotalRow(html=self.html).made_three_point_field_goals, "some made three point field goals")

    def test_made_three_point_field_goals_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(TeamTotalRow(html=self.html).made_three_point_field_goals, '')

    def test_attempted_three_point_field_goals_when_cells_exist(self):
        cell = MagicMock(text_content=MagicMock(return_value="some attempted three point field goals"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(TeamTotalRow(html=self.html).attempted_free_throws, "some attempted three point field goals")

    def test_attempted_three_point_field_goals_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(TeamTotalRow(html=self.html).attempted_three_point_field_goals, '')

    def test_made_free_throws(self):
        cell = MagicMock(text_content=MagicMock(return_value="some made free throws"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(TeamTotalRow(html=self.html).made_free_throws, "some made free throws")

    def test_made_free_throws_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(TeamTotalRow(html=self.html).made_free_throws, '')

    def test_attempted_free_throws(self):
        cell = MagicMock(text_content=MagicMock(return_value="some attempted free throws"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(TeamTotalRow(html=self.html).attempted_free_throws, "some attempted free throws")

    def test_attempted_free_throws_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(TeamTotalRow(html=self.html).attempted_free_throws, '')

    def test_offensive_rebounds(self):
        cell = MagicMock(text_content=MagicMock(return_value="some offensive rebounds"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(TeamTotalRow(html=self.html).offensive_rebounds, "some offensive rebounds")

    def test_offensive_rebounds_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(TeamTotalRow(html=self.html).offensive_rebounds, '')

    def test_defensive_rebounds(self):
        cell = MagicMock(text_content=MagicMock(return_value="some defensive rebounds"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(TeamTotalRow(html=self.html).defensive_rebounds, "some defensive rebounds")

    def test_defensive_rebounds_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(TeamTotalRow(html=self.html).defensive_rebounds, '')

    def test_assists(self):
        cell = MagicMock(text_content=MagicMock(return_value="some assists"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(TeamTotalRow(html=self.html).assists, "some assists")

    def test_assists_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(TeamTotalRow(html=self.html).assists, '')

    def test_steals(self):
        cell = MagicMock(text_content=MagicMock(return_value="some steals"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(TeamTotalRow(html=self.html).steals, "some steals")

    def test_steals_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(TeamTotalRow(html=self.html).steals, '')

    def test_blocks(self):
        cell = MagicMock(text_content=MagicMock(return_value="some blocks"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(TeamTotalRow(html=self.html).blocks, "some blocks")

    def test_blocks_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(TeamTotalRow(html=self.html).blocks, '')

    def test_turnovers(self):
        cell = MagicMock(text_content=MagicMock(return_value="some turnovers"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(TeamTotalRow(html=self.html).turnovers, "some turnovers")

    def test_turnovers_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(TeamTotalRow(html=self.html).turnovers, '')

    def test_personal_fouls(self):
        cell = MagicMock(text_content=MagicMock(return_value="some personal fouls"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(TeamTotalRow(html=self.html).personal_fouls, "some personal fouls")

    def test_personal_fouls_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(TeamTotalRow(html=self.html).personal_fouls, '')

    def test_points(self):
        cell = MagicMock(text_content=MagicMock(return_value="some points"))
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(TeamTotalRow(html=self.html).points, "some points")

    def test_points_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(TeamTotalRow(html=self.html).points, '')
