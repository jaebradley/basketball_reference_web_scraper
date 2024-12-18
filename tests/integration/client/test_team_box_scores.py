import filecmp
import json
import os
from datetime import date
from unittest import TestCase

import basketball_reference_web_scraper.client as client
from basketball_reference_web_scraper.data import OutputWriteOption, OutputType, Team, Outcome
from tests.integration.client.utilities import ResponseMocker


class BoxScoresResponseMocker(ResponseMocker):

    def __init__(self, boxscore_date: date):
        year, month, day = boxscore_date.year, boxscore_date.month, boxscore_date.day
        boxscores_directory = os.path.join(
            os.path.dirname(__file__),
            f"../files/boxscores/{year}/{month}/{day}")

        basketball_reference_paths_by_filename = {}
        for file in os.listdir(os.fsencode(boxscores_directory)):
            filename = os.fsdecode(file)
            if not filename.endswith(".html"):
                raise ValueError(
                    f"Unexpected prefix for {filename}. Expected all files in {boxscores_directory} to end with .html.")

            if filename.startswith("index"):
                key = f"boxscores/?day={day}&month={month}&year={year}"
            else:
                key = f"/boxscores/{filename}"
            basketball_reference_paths_by_filename[os.path.join(boxscores_directory, filename)] = key

        super().__init__(basketball_reference_paths_by_filename=basketball_reference_paths_by_filename)


@BoxScoresResponseMocker(boxscore_date=date(year=2018, month=1, day=1))
class Test20180101TeamBoxScoresInMemoryOutput(TestCase):
    def test_output(self):
        team_box_scores = client.team_box_scores(day=1, month=1, year=2018)
        self.assertListEqual(
            team_box_scores,
            [
                {
                    "team": Team.ORLANDO_MAGIC,
                    "outcome": Outcome.LOSS,
                    "minutes_played": 240,
                    "made_field_goals": 35,
                    "attempted_field_goals": 96,
                    "made_three_point_field_goals": 6,
                    "attempted_three_point_field_goals": 31,
                    "made_free_throws": 19,
                    "attempted_free_throws": 25,
                    "offensive_rebounds": 19,
                    "defensive_rebounds": 33,
                    "assists": 16,
                    "steals": 5,
                    "blocks": 5,
                    "turnovers": 12,
                    "personal_fouls": 18,
                    "points": 95,
                },
                {
                    "team": Team.BROOKLYN_NETS,
                    "outcome": Outcome.WIN,
                    "minutes_played": 240,
                    "made_field_goals": 36,
                    "attempted_field_goals": 82,
                    "made_three_point_field_goals": 9,
                    "attempted_three_point_field_goals": 25,
                    "made_free_throws": 17,
                    "attempted_free_throws": 23,
                    "offensive_rebounds": 10,
                    "defensive_rebounds": 42,
                    "assists": 17,
                    "steals": 7,
                    "blocks": 10,
                    "turnovers": 13,
                    "personal_fouls": 22,
                    "points": 98,
                },
                {
                    "team": Team.PORTLAND_TRAIL_BLAZERS,
                    "outcome": Outcome.WIN,
                    "minutes_played": 265,
                    "made_field_goals": 47,
                    "attempted_field_goals": 108,
                    "made_three_point_field_goals": 14,
                    "attempted_three_point_field_goals": 33,
                    "made_free_throws": 16,
                    "attempted_free_throws": 18,
                    "offensive_rebounds": 12,
                    "defensive_rebounds": 38,
                    "assists": 25,
                    "steals": 7,
                    "blocks": 5,
                    "turnovers": 8,
                    "personal_fouls": 16,
                    "points": 124,
                },
                {
                    "team": Team.CHICAGO_BULLS,
                    "outcome": Outcome.LOSS,
                    "minutes_played": 265,
                    "made_field_goals": 45,
                    "attempted_field_goals": 104,
                    "made_three_point_field_goals": 11,
                    "attempted_three_point_field_goals": 27,
                    "made_free_throws": 19,
                    "attempted_free_throws": 23,
                    "offensive_rebounds": 15,
                    "defensive_rebounds": 43,
                    "assists": 28,
                    "steals": 5,
                    "blocks": 7,
                    "turnovers": 12,
                    "personal_fouls": 21,
                    "points": 120,
                },
                {
                    "team": Team.LOS_ANGELES_LAKERS,
                    "outcome": Outcome.LOSS,
                    "minutes_played": 240,
                    "made_field_goals": 34,
                    "attempted_field_goals": 76,
                    "made_three_point_field_goals": 8,
                    "attempted_three_point_field_goals": 26,
                    "made_free_throws": 20,
                    "attempted_free_throws": 29,
                    "offensive_rebounds": 9,
                    "defensive_rebounds": 28,
                    "assists": 18,
                    "steals": 12,
                    "blocks": 4,
                    "turnovers": 24,
                    "personal_fouls": 25,
                    "points": 96,
                },
                {
                    "team": Team.MINNESOTA_TIMBERWOLVES,
                    "outcome": Outcome.WIN,
                    "minutes_played": 240,
                    "made_field_goals": 40,
                    "attempted_field_goals": 81,
                    "made_three_point_field_goals": 7,
                    "attempted_three_point_field_goals": 20,
                    "made_free_throws": 27,
                    "attempted_free_throws": 30,
                    "offensive_rebounds": 7,
                    "defensive_rebounds": 34,
                    "assists": 26,
                    "steals": 14,
                    "blocks": 5,
                    "turnovers": 17,
                    "personal_fouls": 24,
                    "points": 114,
                },
                {
                    "team": Team.MILWAUKEE_BUCKS,
                    "outcome": Outcome.LOSS,
                    "minutes_played": 265,
                    "made_field_goals": 44,
                    "attempted_field_goals": 93,
                    "made_three_point_field_goals": 13,
                    "attempted_three_point_field_goals": 27,
                    "made_free_throws": 26,
                    "attempted_free_throws": 28,
                    "offensive_rebounds": 10,
                    "defensive_rebounds": 33,
                    "assists": 27,
                    "steals": 9,
                    "blocks": 3,
                    "turnovers": 15,
                    "personal_fouls": 23,
                    "points": 127,
                },
                {
                    "team": Team.TORONTO_RAPTORS,
                    "outcome": Outcome.WIN,
                    "minutes_played": 265,
                    "made_field_goals": 45,
                    "attempted_field_goals": 91,
                    "made_three_point_field_goals": 14,
                    "attempted_three_point_field_goals": 33,
                    "made_free_throws": 27,
                    "attempted_free_throws": 33,
                    "offensive_rebounds": 6,
                    "defensive_rebounds": 34,
                    "assists": 25,
                    "steals": 8,
                    "blocks": 8,
                    "turnovers": 13,
                    "personal_fouls": 20,
                    "points": 131,
                },
            ]
        )


@BoxScoresResponseMocker(boxscore_date=date(year=2001, month=1, day=1))
class Test20010101TeamBoxScoresInMemoryOutput(TestCase):
    def test_length(self):
        team_box_scores = client.team_box_scores(day=1, month=1, year=2001)
        self.assertEqual(4, len(team_box_scores))

    def test_output(self):
        team_box_scores = client.team_box_scores(day=1, month=1, year=2001)
        self.assertTrue({
                            "team": Team.HOUSTON_ROCKETS,
                            "outcome": Outcome.LOSS,
                            "minutes_played": 240,
                            "made_field_goals": 31,
                            "attempted_field_goals": 77,
                            "made_three_point_field_goals": 6,
                            "attempted_three_point_field_goals": 17,
                            "made_free_throws": 28,
                            "attempted_free_throws": 37,
                            "offensive_rebounds": 10,
                            "defensive_rebounds": 26,
                            "assists": 16,
                            "steals": 4,
                            "blocks": 3,
                            "turnovers": 11,
                            "personal_fouls": 19,
                            "points": 96,
                        } in team_box_scores)
        self.assertTrue({
                            "team": Team.MINNESOTA_TIMBERWOLVES,
                            "outcome": Outcome.WIN,
                            "minutes_played": 240,
                            "made_field_goals": 41,
                            "attempted_field_goals": 82,
                            "made_three_point_field_goals": 3,
                            "attempted_three_point_field_goals": 9,
                            "made_free_throws": 21,
                            "attempted_free_throws": 27,
                            "offensive_rebounds": 11,
                            "defensive_rebounds": 36,
                            "assists": 35,
                            "steals": 6,
                            "blocks": 2,
                            "turnovers": 8,
                            "personal_fouls": 29,
                            "points": 106,
                        } in team_box_scores)
        self.assertTrue({
                            "team": Team.CHARLOTTE_HORNETS,
                            "outcome": Outcome.LOSS,
                            "minutes_played": 240,
                            "made_field_goals": 26,
                            "attempted_field_goals": 80,
                            "made_three_point_field_goals": 3,
                            "attempted_three_point_field_goals": 10,
                            "made_free_throws": 12,
                            "attempted_free_throws": 14,
                            "offensive_rebounds": 15,
                            "defensive_rebounds": 26,
                            "assists": 16,
                            "steals": 7,
                            "blocks": 1,
                            "turnovers": 15,
                            "personal_fouls": 25,
                            "points": 67,
                        } in team_box_scores)
        self.assertTrue({
                            "team": Team.PORTLAND_TRAIL_BLAZERS,
                            "outcome": Outcome.WIN,
                            "minutes_played": 240,
                            "made_field_goals": 29,
                            "attempted_field_goals": 70,
                            "made_three_point_field_goals": 4,
                            "attempted_three_point_field_goals": 15,
                            "made_free_throws": 27,
                            "attempted_free_throws": 30,
                            "offensive_rebounds": 11,
                            "defensive_rebounds": 36,
                            "assists": 20,
                            "steals": 8,
                            "blocks": 4,
                            "turnovers": 14,
                            "personal_fouls": 17,
                            "points": 89,
                        } in team_box_scores)


@BoxScoresResponseMocker(boxscore_date=date(year=2018, month=1, day=1))
class TestTeamBoxScoresCSVOutput(TestCase):

    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/team_box_scores/2018/01/01.csv"
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/team_box_scores/2018/01/01.csv"
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def test_output(self):
        client.team_box_scores(
            day=1,
            month=1,
            year=2018,
            output_type=OutputType.CSV,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE
        )

        self.assertTrue(
            filecmp.cmp(
                self.output_file_path,
                self.expected_output_file_path))


@BoxScoresResponseMocker(boxscore_date=date(year=2018, month=1, day=1))
class TestTeamBoxScoresInMemoryJSON(TestCase):
    def setUp(self):
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/team_box_scores/2018/01/01.json"
        )

    def test_output(self):
        results = client.team_box_scores(
            day=1,
            month=1,
            year=2018,
            output_type=OutputType.JSON,
        )
        with open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.loads(results),
                json.load(expected_output_file),
            )


@BoxScoresResponseMocker(boxscore_date=date(year=2018, month=1, day=1))
class TestTeamBoxScoresJSONOutput(TestCase):
    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/team_box_scores/2018/01/01.json"
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/team_box_scores/2018/01/01.json"
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def test_output(self):
        client.team_box_scores(
            day=1,
            month=1,
            year=2018,
            output_type=OutputType.JSON,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE
        )
        self.assertTrue(
            filecmp.cmp(
                self.output_file_path,
                self.expected_output_file_path))
