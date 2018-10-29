from unittest import TestCase

from basketball_reference_web_scraper.data import Outcome, Location
from basketball_reference_web_scraper.parsers import box_scores


class TestSchedule(TestCase):
    def test_parse_seconds_played_for_empty_string(self):
        self.assertEqual(0, box_scores.parse_seconds_played(""))

    def test_parse_seconds_played_for_0_seconds(self):
        self.assertEqual(1, box_scores.parse_seconds_played("0:01"))

    def test_parse_seconds_played_for_59_seconds(self):
        self.assertEqual(59, box_scores.parse_seconds_played("0:59"))

    def test_parse_seconds_played_for_60_seconds(self):
        self.assertEqual(60, box_scores.parse_seconds_played("1:00"))

    def test_parse_seconds_played_for_61_seconds(self):
        self.assertEqual(61, box_scores.parse_seconds_played("1:01"))

    def test_parse_seconds_played_for_59_minutes_59_seconds(self):
        self.assertEqual(3599, box_scores.parse_seconds_played("59:59"))

    def test_parse_seconds_played_for_60_minutes(self):
        self.assertEqual(3600, box_scores.parse_seconds_played("60:00"))

    def test_parse_seconds_played_for_60_minutes_and_1_second(self):
        self.assertEqual(3601, box_scores.parse_seconds_played("60:01"))

    def test_parse_win(self):
        self.assertEqual(Outcome.WIN, box_scores.parse_outcome("W"))

    def test_parse_loss(self):
        self.assertEqual(Outcome.LOSS, box_scores.parse_outcome("L"))

    def test_parse_unknown_outcome_symbol(self):
        self.assertRaises(ValueError, box_scores.parse_outcome, "jaebaebae")

    def test_parse_away_symbol(self):
        self.assertEqual(Location.AWAY, box_scores.parse_location("@"))

    def test_parse_home_symbol(self):
        self.assertEqual(Location.HOME, box_scores.parse_location(""))

    def test_parse_unknown_location_symbol(self):
        self.assertRaises(ValueError, box_scores.parse_location, "jaebaebae")
