from unittest import TestCase
import datetime

from basketball_reference_web_scraper.models.event import Event


class TestEvent(TestCase):
    def test_expected(self):
        test_date = datetime.datetime.strptime("1990-01-01", "%Y-%m-%d")
        visiting_team_name = "test_visiting_team_name"
        home_team_name = "test_home_team_name"
        test_event = Event(
            test_date,
            visiting_team_name,
            home_team_name
        )

        assert test_date == test_event.start_time
        assert visiting_team_name == test_event.visiting_team_name
        assert home_team_name == test_event.home_team_name

    def test_assertions(self):
        test_date = datetime.datetime.strptime("1990-01-01", "%Y-%m-%d")
        visiting_team_name = "test_visiting_team_name"
        home_team_name = "test_home_team_name"

        self.assertRaises(AssertionError, Event, None, visiting_team_name, home_team_name)
        self.assertRaises(AssertionError, Event, test_date, None, home_team_name)
        self.assertRaises(AssertionError, Event, test_date, visiting_team_name, None)