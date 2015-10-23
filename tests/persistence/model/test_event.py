from unittest import TestCase
from src.persistence.model.event import Event
import datetime


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

    def test_none(self):
        test_date = datetime.datetime.strptime("1990-01-01", "%Y-%m-%d")
        visiting_team_name = "test_visiting_team_name"
        home_team_name = "test_home_team_name"

        try:
            test_event = Event(
                None,
                visiting_team_name,
                home_team_name
            )
            assert False, "should not reach this point"
        except AssertionError:
            pass
            # expected

        try:
            test_event = Event(
                test_date,
                None,
                home_team_name
            )
            assert False, "should not reach this point"
        except AssertionError:
            pass
            # expected

        try:
            test_event = Event(
                test_date,
                visiting_team_name,
                None
            )
            assert False, "should not reach this point"
        except AssertionError:
            pass
            # expected