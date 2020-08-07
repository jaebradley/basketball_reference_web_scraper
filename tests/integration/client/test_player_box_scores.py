import os
from unittest import TestCase
import json

from basketball_reference_web_scraper.client import player_box_scores
from basketball_reference_web_scraper.data import OutputType, OutputWriteOption
from basketball_reference_web_scraper.errors import InvalidDate


class TestInMemoryPlayerBoxScores(TestCase):
    def test_2018_01_01_player_box_scores_length(self):
        result = player_box_scores(day=1, month=1, year=2018)
        self.assertEqual(len(result), 82)

    def test_2001_01_01_player_box_scores_length(self):
        result = player_box_scores(day=1, month=1, year=2001)
        self.assertEqual(len(result), 39)


class TestCSVPlayerBoxScoresFor20010101(TestCase):
    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/2001_01_01_player_box_scores.csv",
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2001_01_01_player_box_scores.csv",
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def test_2001_01_01_player_box_scores(self):
        player_box_scores(
            day=1, month=1, year=2001,
            output_type=OutputType.CSV,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )
        with open(self.output_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(output_file.readlines(), expected_output_file.readlines())


class TestJSONPlayerBoxScores20010101(TestCase):
    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/2001_01_01_player_box_scores.json",
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2001_01_01_player_box_scores.json",
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def test_2001_01_01_player_box_scores(self):
        player_box_scores(
            day=1, month=1, year=2001,
            output_type=OutputType.JSON,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )

        with open(self.output_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.load(output_file),
                json.load(expected_output_file),
            )


class TestInMemoryJSONPlayerBoxScores20010101(TestCase):
    def setUp(self):
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2001_01_01_player_box_scores.json",
        )

    def test_2001_01_01_player_box_scores(self):
        box_scores = player_box_scores(
            day=1, month=1, year=2001,
            output_type=OutputType.JSON,
        )

        with open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.loads(box_scores),
                json.load(expected_output_file),
            )


class TestPlayerBoxScores(TestCase):
    def test_get_box_scores_for_day_that_does_not_exist(self):
        self.assertRaisesRegex(
            InvalidDate,
            "Date with year set to 2018, month set to 1, and day set to -1 is invalid",
            player_box_scores,
            day=-1, month=1, year=2018)

    def test_raises_invalid_date_for_nonexistent_dates(self):
        self.assertRaisesRegex(
            InvalidDate,
            "Date with year set to baz, month set to bar, and day set to foo is invalid",
            player_box_scores,
            day="foo", month="bar", year="baz")
