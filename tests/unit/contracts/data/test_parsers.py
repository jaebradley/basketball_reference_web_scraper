from unittest import TestCase

from basketball_reference_web_scraper.contracts.data.parsers import deserialize_season_start_year


class TestDeserializingSeasonStartYear(TestCase):
    def test_non_numeric_value_raises_error(self):
        with self.assertRaises(ValueError):
            deserialize_season_start_year(serialized_season="foobar")

    def test_invalidly_formatted_numeric_value_raises_error(self):
        with self.assertRaises(ValueError):
            deserialize_season_start_year(serialized_season="2024")

    def test_validly_formatted_value_returns_value(self):
        assert 2024 == deserialize_season_start_year(serialized_season="2024-25")
