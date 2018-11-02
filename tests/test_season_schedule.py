from unittest import TestCase

from basketball_reference_web_scraper.client import season_schedule
from basketball_reference_web_scraper.data import OutputType, OutputWriteOption


class TestSeason_schedule(TestCase):
    def test_season_schedule(self):
        result = season_schedule(season_end_year=2018)
        self.assertIsNotNone(result)

    def test_season_schedule_json(self):
        result = season_schedule(season_end_year=2018, output_type=OutputType.JSON)
        self.assertIsNotNone(result)

    def test_season_schedule_csv(self):
        season_schedule(season_end_year=2018, output_type=OutputType.CSV, output_file_path="./foo.csv")

    def test_season_schedule_csv_append(self):
        season_schedule(season_end_year=2018, output_type=OutputType.CSV, output_file_path="./foo.csv", output_write_option=OutputWriteOption.WRITE)

    def test_2017_season_schedule_csv_append(self):
        season_schedule(season_end_year=2001, output_type=OutputType.CSV, output_file_path="./foo.csv", output_write_option=OutputWriteOption.WRITE)
