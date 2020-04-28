from unittest import TestCase

from basketball_reference_web_scraper.parser_service import ParserService
from basketball_reference_web_scraper.parsers import ResourceLocationParser


class TestResourceLocationParser(TestCase):
    def setUp(self):
        self.parser = ResourceLocationParser(resource_location_regex=ParserService.SEARCH_RESULT_RESOURCE_LOCATION_REGEX)

    def test_parse_players_resource_type(self):
        self.assertEqual(
            self.parser.parse_resource_type(
                resource_location="https://www.basketball-reference.com/players/k/koperbu01.html"
            ),
            "players"
        )

    def test_parse_coaches_resource_type(self):
        self.assertEqual(
            self.parser.parse_resource_type(
                resource_location="https://www.basketball-reference.com/coaches/vanbrbu01c.html"
            ),
            "coaches"
        )

    def test_parse_executives_resource_type(self):
        self.assertEqual(
            self.parser.parse_resource_type(
                resource_location="https://www.basketball-reference.com/executives/vanbrbu01x.html"
            ),
            "executives",
        )

    def test_parse_players_resource_identifier(self):
        self.assertEqual(
            self.parser.parse_resource_identifier(
                resource_location="https://www.basketball-reference.com/players/k/koperbu01.html"
            ),
            "koperbu01"
        )

    def test_parse_coaches_resource_identifier(self):
        self.assertEqual(
            self.parser.parse_resource_identifier(
                resource_location="https://www.basketball-reference.com/coaches/vanbrbu01c.html"
            ),
            "vanbrbu01c"
        )

    def test_parse_executives_resource_identifier(self):
        self.assertEqual(
            self.parser.parse_resource_identifier(
                resource_location="https://www.basketball-reference.com/executives/vanbrbu01x.html"
            ),
            "vanbrbu01x",
        )
