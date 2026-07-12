from unittest import TestCase

from basketball_reference_web_scraper.contracts.data.parsers import SalariesBySeasonParser


class TestSalariesBySeasonParser(TestCase):
    def setUp(self):
        self.parser = SalariesBySeasonParser(
            season_start_year_deserializer=None
        )

    def test_unknown_column_name_raises_error(self):
        raise NotImplementedError()

    def test_season_start_year_deserialization_error_raises_error(self):
        raise NotImplementedError()

    def test_salary_deserialization_error_raises_error(self):
        raise NotImplementedError()