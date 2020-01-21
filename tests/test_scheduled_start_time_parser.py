from datetime import datetime, timedelta
from unittest import TestCase

import pytz

from basketball_reference_web_scraper.parsers import ScheduledStartTimeParser


class TestScheduledStartTimeParser(TestCase):
    def test_correctly_parses_time_for_current_pm_formatting(self):
        parsed_start_time = ScheduledStartTimeParser().parse_start_time(
            formatted_date="Tue, Oct 17, 2017",
            formatted_time_of_day="8:01p"
        )
        expected_datetime = pytz.timezone("US/Eastern")\
            .localize(datetime(year=2017, month=10, day=17, hour=20, minute=1))\
            .astimezone(pytz.utc)

        self.assertTrue(abs(parsed_start_time - expected_datetime) < timedelta(seconds=1))

    def test_correctly_parses_time_for_current_am_formatting(self):
        parsed_start_time = ScheduledStartTimeParser().parse_start_time(
            formatted_date="Tue, Oct 17, 2017",
            formatted_time_of_day="8:01a"
        )
        expected_datetime = pytz.timezone("US/Eastern") \
            .localize(datetime(year=2017, month=10, day=17, hour=8, minute=1)) \
            .astimezone(pytz.utc)

        self.assertTrue(abs(parsed_start_time - expected_datetime) < timedelta(seconds=1))

    def test_correctly_parses_time_for_previous_pm_formatting(self):
        parsed_start_time = ScheduledStartTimeParser().parse_start_time(
            formatted_date="Tue, Oct 17, 2017",
            formatted_time_of_day="7:30 pm"
        )
        expected_datetime = pytz.timezone("US/Eastern") \
            .localize(datetime(year=2017, month=10, day=17, hour=19, minute=30)) \
            .astimezone(pytz.utc)

        self.assertTrue(abs(parsed_start_time - expected_datetime) < timedelta(seconds=1))

    def test_correctly_parses_time_for_previous_am_formatting(self):
        parsed_start_time = ScheduledStartTimeParser().parse_start_time(
            formatted_date="Tue, Oct 17, 2017",
            formatted_time_of_day="7:30 am"
        )
        expected_datetime = pytz.timezone("US/Eastern") \
            .localize(datetime(year=2017, month=10, day=17, hour=7, minute=30)) \
            .astimezone(pytz.utc)

        self.assertTrue(abs(parsed_start_time - expected_datetime) < timedelta(seconds=1))
