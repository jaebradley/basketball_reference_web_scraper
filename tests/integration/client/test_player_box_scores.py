import csv
import filecmp
import json
import os
from tempfile import TemporaryDirectory
from unittest import TestCase

import requests_mock

from basketball_reference_web_scraper.client import player_box_scores
from basketball_reference_web_scraper.data import OutputType, OutputWriteOption
from basketball_reference_web_scraper.errors import InvalidDate


class Test20180101(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/player_box_scores/2018/1/1.html"
        ), 'r') as file_input: self._html = file_input.read()

    @requests_mock.Mocker()
    def test_player_box_scores_length(self, m):
        m.get("https://www.basketball-reference.com/friv/dailyleaders.cgi?month=1&day=1&year=2018",
              text=self._html,
              status_code=200)
        result = player_box_scores(day=1, month=1, year=2018)
        self.assertEqual(len(result), 82)


class Test20010101(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/player_box_scores/2001/1/1.html"
        ), 'r') as file_input: self._html = file_input.read()

    @requests_mock.Mocker()
    def test_2001_01_01_player_box_scores_length(self, m):
        m.get("https://www.basketball-reference.com/friv/dailyleaders.cgi?month=1&day=1&year=2001",
              text=self._html,
              status_code=200)
        result = player_box_scores(day=1, month=1, year=2001)
        self.assertEqual(len(result), 39)

    @requests_mock.Mocker()
    def test_json_output(self, m):
        m.get("https://www.basketball-reference.com/friv/dailyleaders.cgi?month=1&day=1&year=2001",
              text=self._html,
              status_code=200)

        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/player_box_scores/2001/1/1.json",
        )

        try:
            player_box_scores(
                day=1, month=1, year=2001,
                output_type=OutputType.JSON,
                output_file_path=output_file_path,
                output_write_option=OutputWriteOption.WRITE,
            )
            self.assertTrue(
                filecmp.cmp(
                    output_file_path,
                    os.path.join(
                        os.path.dirname(__file__),
                        "./output/expected/player_box_scores/2001/1/1.json",
                    )))
        finally:
            os.remove(output_file_path)

    @requests_mock.Mocker()
    def test_in_memory_json_output(self, m):
        m.get("https://www.basketball-reference.com/friv/dailyleaders.cgi?month=1&day=1&year=2001",
              text=self._html,
              status_code=200)

        box_scores = player_box_scores(
            day=1, month=1, year=2001,
            output_type=OutputType.JSON,
        )

        with open(os.path.join(
                os.path.dirname(__file__),
                "./output/expected/player_box_scores/2001/1/1.json",
        ), "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.loads(box_scores),
                json.load(expected_output_file),
            )

    @requests_mock.Mocker()
    def test_csv_output(self, m):
        m.get("https://www.basketball-reference.com/friv/dailyleaders.cgi?month=1&day=1&year=2001",
              text=self._html,
              status_code=200)

        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/player_box_scores/2001/1/1.csv",
        )
        try:
            player_box_scores(
                day=1, month=1, year=2001,
                output_type=OutputType.CSV,
                output_file_path=output_file_path,
                output_write_option=OutputWriteOption.WRITE,
            )
            self.assertTrue(
                filecmp.cmp(
                    output_file_path,
                    os.path.join(
                        os.path.dirname(__file__),
                        "./output/expected/player_box_scores/2001/1/1.csv",
                    )))
        finally:
            os.remove(output_file_path)

    @requests_mock.Mocker()
    def test_csv_append_preserves_box_score_rows(self, m):
        m.get("https://www.basketball-reference.com/friv/dailyleaders.cgi?month=1&day=1&year=2001",
              text=self._html,
              status_code=200)

        for mode in (OutputWriteOption.APPEND, OutputWriteOption.APPEND_AND_WRITE):
            with self.subTest(mode=mode), TemporaryDirectory() as directory:
                output_file_path = os.path.join(directory, "box_scores.csv")
                for _ in range(2):
                    player_box_scores(
                        day=1, month=1, year=2001,
                        output_type=OutputType.CSV,
                        output_file_path=output_file_path,
                        output_write_option=mode,
                    )

                with open(output_file_path, newline="", encoding="utf8") as output:
                    rows = list(csv.DictReader(output))
                self.assertEqual(78, len(rows))
                self.assertEqual(rows[:39], rows[39:])


class TestPlayerBoxScores(TestCase):
    @requests_mock.Mocker()
    def test_get_box_scores_for_day_that_does_not_exist(self, m):
        m.get("https://www.basketball-reference.com/friv/dailyleaders.cgi?month=1&day=-1&year=2018",
              text="Not found",
              status_code=404)
        self.assertRaisesRegex(
            InvalidDate,
            "Date with year set to 2018, month set to 1, and day set to -1 is invalid",
            player_box_scores,
            day=-1, month=1, year=2018)

