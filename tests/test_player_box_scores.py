from unittest import TestCase

from basketball_reference_web_scraper.client import player_box_scores
from basketball_reference_web_scraper.data import OutputType, OutputWriteOption
from basketball_reference_web_scraper.errors import InvalidDate


class TestPlayerBoxScores(TestCase):
    def test_get_box_scores(self):
        result = player_box_scores(day=1, month=1, year=2018)
        self.assertIsNotNone(result)

    def test_get_box_scores_for_day_that_does_not_exist(self):
        self.assertRaises(InvalidDate, player_box_scores, day=-1, month=1, year=2018)

    def test_get_box_scores_from_2001(self):
        player_box_scores(day=1, month=1, year=2001, output_type=OutputType.CSV, output_file_path="./foo.csv", output_write_option=OutputWriteOption.WRITE)