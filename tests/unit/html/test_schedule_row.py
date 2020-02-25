from unittest import TestCase
from unittest.mock import MagicMock

from basketball_reference_web_scraper.html import ScheduleRow


class TestScheduleRow(TestCase):
    def setUp(self):
        self.html = MagicMock()

    def test_instance_is_not_equal_to_different_class_instance(self):
        self.assertNotEqual(ScheduleRow(html=MagicMock()), 1)

    def test_instance_is_not_equal_to_same_class_instance_if_html_is_different(self):
        self.assertNotEqual(ScheduleRow(html=MagicMock()), ScheduleRow(html=MagicMock()))

    def test_start_date_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[MagicMock(text_content=MagicMock(return_value="some start date"))])
        self.assertEqual(ScheduleRow(html=self.html).start_date, "some start date")
        self.html.xpath.assert_called_once_with('th[@data-stat="date_game"]')

    def test_start_date_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(ScheduleRow(html=self.html).start_date, "")
        self.html.xpath.assert_called_once_with('th[@data-stat="date_game"]')

    def test_start_time_of_day_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[MagicMock(text_content=MagicMock(return_value="some start time of day"))])
        self.assertEqual(ScheduleRow(html=self.html).start_time_of_day, "some start time of day")
        self.html.xpath.assert_called_once_with('td[@data-stat="game_start_time"]')

    def test_start_time_of_day_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(ScheduleRow(html=self.html).start_time_of_day, "")
        self.html.xpath.assert_called_once_with('td[@data-stat="game_start_time"]')

    def test_away_team_name_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[MagicMock(text_content=MagicMock(return_value="some away team name"))])
        self.assertEqual(ScheduleRow(html=self.html).away_team_name, "some away team name")
        self.html.xpath.assert_called_once_with('td[@data-stat="visitor_team_name"]')

    def test_away_team_name_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(ScheduleRow(html=self.html).away_team_name, "")
        self.html.xpath.assert_called_once_with('td[@data-stat="visitor_team_name"]')

    def test_home_team_name_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[MagicMock(text_content=MagicMock(return_value="some home team name"))])
        self.assertEqual(ScheduleRow(html=self.html).home_team_name, "some home team name")
        self.html.xpath.assert_called_once_with('td[@data-stat="home_team_name"]')

    def test_home_team_name_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(ScheduleRow(html=self.html).home_team_name, "")
        self.html.xpath.assert_called_once_with('td[@data-stat="home_team_name"]')

    def test_away_team_score_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[MagicMock(text_content=MagicMock(return_value="some away team score"))])
        self.assertEqual(ScheduleRow(html=self.html).away_team_score, "some away team score")
        self.html.xpath.assert_called_once_with('td[@data-stat="visitor_pts"]')

    def test_away_team_score_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(ScheduleRow(html=self.html).away_team_score, "")
        self.html.xpath.assert_called_once_with('td[@data-stat="visitor_pts"]')

    def test_home_team_score_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[MagicMock(text_content=MagicMock(return_value="some home team score"))])
        self.assertEqual(ScheduleRow(html=self.html).home_team_score, "some home team score")
        self.html.xpath.assert_called_once_with('td[@data-stat="home_pts"]')

    def test_home_team_score_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(ScheduleRow(html=self.html).home_team_score, "")
        self.html.xpath.assert_called_once_with('td[@data-stat="home_pts"]')
