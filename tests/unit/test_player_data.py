from unittest import TestCase

from basketball_reference_web_scraper.data import PlayerData


class TestPlayerData(TestCase):
    def test_instantiation(self):
        data = PlayerData(
            name="some name",
            resource_location="some location",
            league_abbreviations=["NBA", "ABA", "NBA", "ABA"],
        )
        self.assertEqual(data.name, "some name")
        self.assertEqual(data.resource_location, "some location")
        self.assertEqual(data.league_abbreviations, {"NBA", "ABA"})
