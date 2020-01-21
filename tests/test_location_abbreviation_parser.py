from unittest import TestCase

from basketball_reference_web_scraper.data import Location, LOCATION_ABBREVIATIONS_TO_POSITION
from basketball_reference_web_scraper.parsers import LocationAbbreviationParser


class TestLocationAbbreviationParser(TestCase):
    def setUp(self):
        self.parser = LocationAbbreviationParser(abbreviations_to_locations=LOCATION_ABBREVIATIONS_TO_POSITION)

    def test_parse_away_symbol(self):
        self.assertEqual(Location.AWAY, self.parser.from_abbreviation("@"))

    def test_parse_home_symbol(self):
        self.assertEqual(Location.HOME, self.parser.from_abbreviation(""))

    def test_parse_unknown_location_symbol(self):
        self.assertRaises(ValueError, self.parser.from_abbreviation, "jaebaebae")