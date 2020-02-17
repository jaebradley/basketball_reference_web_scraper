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

    def test_start_date(self):
        start_date = "some start date"
        start_date_cell = MagicMock()
        start_date_cell.text_content = MagicMock(return_value=start_date)
        self.html.__getitem__ = MagicMock(return_value=start_date_cell)

        self.assertEqual(ScheduleRow(html=self.html).start_date, start_date)
        self.html.__getitem__.assert_called_once_with(0)
        start_date_cell.text_content.assert_called_once_with()

    def test_start_time_of_day(self):
        start_time_of_day = "some start time of day"
        start_time_of_day_cell = MagicMock()
        start_time_of_day_cell.text_content = MagicMock(return_value=start_time_of_day)
        self.html.__getitem__ = MagicMock(return_value=start_time_of_day_cell)

        self.assertEqual(ScheduleRow(html=self.html).start_time_of_day, start_time_of_day)
        self.html.__getitem__.assert_called_once_with(1)
        start_time_of_day_cell.text_content.assert_called_once_with()

    def test_away_team_name(self):
        away_team_name = "some away team name"
        away_team_name_cell = MagicMock()
        away_team_name_cell.text_content = MagicMock(return_value=away_team_name)
        self.html.__getitem__ = MagicMock(return_value=away_team_name_cell)

        self.assertEqual(ScheduleRow(html=self.html).away_team_name, away_team_name)
        self.html.__getitem__.assert_called_once_with(2)
        away_team_name_cell.text_content.assert_called_once_with()

    def test_home_team_name(self):
        home_team_name = "some home team name"
        home_team_name_cell = MagicMock()
        home_team_name_cell.text_content = MagicMock(return_value=home_team_name)
        self.html.__getitem__ = MagicMock(return_value=home_team_name_cell)

        self.assertEqual(ScheduleRow(html=self.html).home_team_name, home_team_name)
        self.html.__getitem__.assert_called_once_with(4)
        home_team_name_cell.text_content.assert_called_once_with()

    def test_away_team_score(self):
        away_team_score = "some away team score"
        away_team_score_cell = MagicMock()
        away_team_score_cell.text_content = MagicMock(return_value=away_team_score)
        self.html.__getitem__ = MagicMock(return_value=away_team_score_cell)

        self.assertEqual(ScheduleRow(html=self.html).away_team_score, away_team_score)
        self.html.__getitem__.assert_called_once_with(3)
        away_team_score_cell.text_content.assert_called_once_with()

    def test_home_team_score(self):
        home_team_score = "some home team score"
        home_team_score_cell = MagicMock()
        home_team_score_cell.text_content = MagicMock(return_value=home_team_score)
        self.html.__getitem__ = MagicMock(return_value=home_team_score_cell)

        self.assertEqual(ScheduleRow(html=self.html).home_team_score, home_team_score)
        self.html.__getitem__.assert_called_once_with(5)
        home_team_score_cell.text_content.assert_called_once_with()
