from unittest import TestCase

from basketball_reference_web_scraper.data import Outcome, Location
from basketball_reference_web_scraper.parsers.box_scores import players


class TestBoxScores(TestCase):
    def test_parse_seconds_played_for_empty_string(self):
        self.assertEqual(0, players.parse_seconds_played(""))

    def test_parse_seconds_played_for_0_seconds(self):
        self.assertEqual(1, players.parse_seconds_played("0:01"))

    def test_parse_seconds_played_for_59_seconds(self):
        self.assertEqual(59, players.parse_seconds_played("0:59"))

    def test_parse_seconds_played_for_60_seconds(self):
        self.assertEqual(60, players.parse_seconds_played("1:00"))

    def test_parse_seconds_played_for_61_seconds(self):
        self.assertEqual(61, players.parse_seconds_played("1:01"))

    def test_parse_seconds_played_for_59_minutes_59_seconds(self):
        self.assertEqual(3599, players.parse_seconds_played("59:59"))

    def test_parse_seconds_played_for_60_minutes(self):
        self.assertEqual(3600, players.parse_seconds_played("60:00"))

    def test_parse_seconds_played_for_60_minutes_and_1_second(self):
        self.assertEqual(3601, players.parse_seconds_played("60:01"))

    def test_parse_win(self):
        self.assertEqual(Outcome.WIN, players.parse_outcome("W"))

    def test_parse_loss(self):
        self.assertEqual(Outcome.LOSS, players.parse_outcome("L"))

    def test_parse_unknown_outcome_symbol(self):
        self.assertRaises(ValueError, players.parse_outcome, "jaebaebae")

    def test_parse_away_symbol(self):
        self.assertEqual(Location.AWAY, players.parse_location("@"))

    def test_parse_home_symbol(self):
        self.assertEqual(Location.HOME, players.parse_location(""))

    def test_parse_unknown_location_symbol(self):
        self.assertRaises(ValueError, players.parse_location, "jaebaebae")