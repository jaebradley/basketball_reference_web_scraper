from unittest import TestCase

from basketball_reference_web_scraper.data import Team, Location, Outcome, Position
from basketball_reference_web_scraper.output.fields import format_value


class TestRowFormatter(TestCase):
    def test_team_enum_value(self):
        self.assertEqual(format_value(Team.BOSTON_CELTICS), "BOSTON CELTICS")

    def test_location_enum_value(self):
        self.assertEqual(format_value(Location.HOME), "HOME")

    def test_outcome_enum_value(self):
        self.assertEqual(format_value(Outcome.LOSS), "LOSS")

    def test_empty_array(self):
        self.assertEqual(format_value([]), "")

    def test_empty_set(self):
        self.assertEqual(format_value(set()), "")

    def test_position_enum_value(self):
        self.assertEqual(format_value(Position.POINT_GUARD), "POINT GUARD")

    def test_positions_array_with_single_position(self):
        self.assertEqual(format_value([Position.POINT_GUARD]), "POINT GUARD")

    def test_positions_array_with_multiple_positions(self):
        self.assertEqual(format_value([Position.POINT_GUARD, Position.SHOOTING_GUARD]), "POINT GUARD-SHOOTING GUARD")

    def test_positions_set_with_single_position(self):
        self.assertEqual(format_value({Position.POINT_GUARD}), "POINT GUARD")

    def test_string_value(self):
        self.assertEqual(format_value("jaebaebae"), "jaebaebae")
