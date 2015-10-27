from unittest import TestCase

from basketball_reference_web_scraper.helper_functions.schedule.season_schedule_url_generator import SeasonScheduleUrlGenerator


class TestScheduleUrlGenerator(TestCase):
    def test_expected(self):
        test_year = 2014
        result = SeasonScheduleUrlGenerator.generate_url(test_year)
        expected_result = "http://www.basketball-reference.com/leagues/NBA_{0}_games.html".format(test_year)
        assert expected_result == result

    def test_assertions(self):

        self.assertRaises(AssertionError, SeasonScheduleUrlGenerator.generate_url, None)
        self.assertRaises(AssertionError, SeasonScheduleUrlGenerator.generate_url, "Foo")