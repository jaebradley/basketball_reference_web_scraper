from unittest import TestCase

from client import season_schedule
from data import OutputType


class TestSeason_schedule(TestCase):
    def test_season_schedule(self):
        result = season_schedule(season_end_year=2018)
        self.assertIsNotNone(result)

    def test_season_schedule_json(self):
        result = season_schedule(season_end_year=2018, output_type=OutputType.JSON)
        self.assertIsNotNone(result)

    def test_season_schedule_csv(self):
        season_schedule(season_end_year=2018, output_type=OutputType.CSV, output_file_path="./foo.csv")
