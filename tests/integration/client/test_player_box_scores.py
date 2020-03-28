import os
from unittest import TestCase

from basketball_reference_web_scraper.client import player_box_scores
from basketball_reference_web_scraper.data import OutputType, OutputWriteOption
from basketball_reference_web_scraper.errors import InvalidDate


class TestPlayerBoxScores(TestCase):
    def test_get_box_scores(self):
        result = player_box_scores(day=1, month=1, year=2018)
        self.assertIsNotNone(result)

    def test_get_box_scores_for_day_that_does_not_exist(self):
        self.assertRaisesRegex(
            InvalidDate,
            "Date with year set to 2018, month set to 1, and day set to -1 is invalid",
            player_box_scores,
            day=-1, month=1, year=2018)

    def test_get_box_scores_from_2001(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/2003_10_29_TOR_pbp.csv",
        )
        player_box_scores(
            day=1, month=1, year=2001,
            output_type=OutputType.CSV, output_file_path=output_file_path, output_write_option=OutputWriteOption.WRITE)

    def test_raises_invalid_date_for_nonexistent_dates(self):
        self.assertRaisesRegex(
            InvalidDate,
            "Date with year set to baz, month set to bar, and day set to foo is invalid",
            player_box_scores,
            day="foo", month="bar", year="baz")
