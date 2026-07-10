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
                    "assist_percentage": 45.7,
                    "assists": 16,
                    "attempted_field_goals": 96,
                    "attempted_free_throws": 25,
                    "attempted_three_point_field_goals": 31,
                    "block_percentage": 8.8,
                    "blocks": 5,
                    "defensive_rating": 102.9,
                    "defensive_rebound_percentage": 76.7,
                    "defensive_rebounds": 33,
                    "effective_field_goal_percentage": 0.396,
                    "free_throw_attempt_rate": 0.26,
                    "made_field_goals": 35,
                    "made_free_throws": 19,
                    "made_three_point_field_goals": 6,
                    "minutes_played": 240,
                    "offensive_rating": 99.8,
                    "offensive_rebound_percentage": 31.1,
                    "offensive_rebounds": 19,
                    "outcome": Outcome.LOSS,
                    "personal_fouls": 18,
                    "points": 95,
                    "steal_percentage": 5.3,
                    "steals": 5,
                    "team": Team.ORLANDO_MAGIC,
                    "three_point_attempt_rate": 0.323,
                    "total_rebound_percentage": 50.0,
                    "true_shooting_percentage": 0.444,
                    "turnover_rate": 10.1,
                    "turnovers": 12
                },
                {
                    "assist_percentage": 47.2,
                    "assists": 17,
                    "attempted_field_goals": 82,
                    "attempted_free_throws": 23,
                    "attempted_three_point_field_goals": 25,
                    "block_percentage": 15.4,
                    "blocks": 10,
                    "defensive_rating": 99.8,
                    "defensive_rebound_percentage": 68.9,
                    "defensive_rebounds": 42,
                    "effective_field_goal_percentage": 0.494,
                    "free_throw_attempt_rate": 0.28,
                    "made_field_goals": 36,
                    "made_free_throws": 17,
                    "made_three_point_field_goals": 9,
                    "minutes_played": 240,
                    "offensive_rating": 102.9,
                    "offensive_rebound_percentage": 23.3,
                    "offensive_rebounds": 10,
                    "outcome": Outcome.WIN,
                    "personal_fouls": 22,
                    "points": 98,
                    "steal_percentage": 7.4,
                    "steals": 7,
                    "team": Team.BROOKLYN_NETS,
                    "three_point_attempt_rate": 0.305,
                    "total_rebound_percentage": 50.0,
                    "true_shooting_percentage": 0.532,
                    "turnover_rate": 12.4,
                    "turnovers": 13
                },
                {
                    "assist_percentage": 53.2,
                    "assists": 25,
                    "attempted_field_goals": 108,
                    "attempted_free_throws": 18,
                    "attempted_three_point_field_goals": 33,
                    "block_percentage": 6.5,
                    "blocks": 5,
                    "defensive_rating": 111.0,
                    "defensive_rebound_percentage": 71.7,
                    "defensive_rebounds": 38,
                    "effective_field_goal_percentage": 0.5,
                    "free_throw_attempt_rate": 0.167,
                    "made_field_goals": 47,
                    "made_free_throws": 16,
                    "made_three_point_field_goals": 14,
                    "minutes_played": 265,
                    "offensive_rating": 114.7,
                    "offensive_rebound_percentage": 21.8,
                    "offensive_rebounds": 12,
                    "outcome": Outcome.WIN,
                    "personal_fouls": 16,
                    "points": 124,
                    "steal_percentage": 6.5,
                    "steals": 7,
                    "team": Team.PORTLAND_TRAIL_BLAZERS,
                    "three_point_attempt_rate": 0.306,
                    "total_rebound_percentage": 46.3,
                    "true_shooting_percentage": 0.535,
                    "turnover_rate": 6.5,
                    "turnovers": 8
                },
                {
                    "assist_percentage": 62.2,
                    "assists": 28,
                    "attempted_field_goals": 104,
                    "attempted_free_throws": 23,
                    "attempted_three_point_field_goals": 27,
                    "block_percentage": 9.3,
                    "blocks": 7,
                    "defensive_rating": 114.7,
                    "defensive_rebound_percentage": 78.2,
                    "defensive_rebounds": 43,
                    "effective_field_goal_percentage": 0.486,
                    "free_throw_attempt_rate": 0.221,
                    "made_field_goals": 45,
                    "made_free_throws": 19,
                    "made_three_point_field_goals": 11,
                    "minutes_played": 265,
                    "offensive_rating": 111.0,
                    "offensive_rebound_percentage": 28.3,
                    "offensive_rebounds": 15,
                    "outcome": Outcome.LOSS,
                    "personal_fouls": 21,
                    "points": 120,
                    "steal_percentage": 4.6,
                    "steals": 5,
                    "team": Team.CHICAGO_BULLS,
                    "three_point_attempt_rate": 0.26,
                    "total_rebound_percentage": 53.7,
                    "true_shooting_percentage": 0.526,
                    "turnover_rate": 9.5,
                    "turnovers": 12
                },
                {
                    "assist_percentage": 52.9,
                    "assists": 18,
                    "attempted_field_goals": 76,
                    "attempted_free_throws": 29,
                    "attempted_three_point_field_goals": 26,
                    "block_percentage": 6.6,
                    "blocks": 4,
                    "defensive_rating": 112.1,
                    "defensive_rebound_percentage": 80.0,
                    "defensive_rebounds": 28,
                    "effective_field_goal_percentage": 0.5,
                    "free_throw_attempt_rate": 0.382,
                    "made_field_goals": 34,
                    "made_free_throws": 20,
                    "made_three_point_field_goals": 8,
                    "minutes_played": 240,
                    "offensive_rating": 94.4,
                    "offensive_rebound_percentage": 20.9,
                    "offensive_rebounds": 9,
                    "outcome": Outcome.LOSS,
                    "personal_fouls": 25,
                    "points": 96,
                    "steal_percentage": 11.8,
                    "steals": 12,
                    "team": Team.LOS_ANGELES_LAKERS,
                    "three_point_attempt_rate": 0.342,
                    "total_rebound_percentage": 47.4,
                    "true_shooting_percentage": 0.541,
                    "turnover_rate": 21.3,
                    "turnovers": 24
                },
                {
                    "assist_percentage": 65.0,
                    "assists": 26,
                    "attempted_field_goals": 81,
                    "attempted_free_throws": 30,
                    "attempted_three_point_field_goals": 20,
                    "block_percentage": 10.0,
                    "blocks": 5,
                    "defensive_rating": 94.4,
                    "defensive_rebound_percentage": 79.1,
                    "defensive_rebounds": 34,
                    "effective_field_goal_percentage": 0.537,
                    "free_throw_attempt_rate": 0.37,
                    "made_field_goals": 40,
                    "made_free_throws": 27,
                    "made_three_point_field_goals": 7,
                    "minutes_played": 240,
                    "offensive_rating": 112.1,
                    "offensive_rebound_percentage": 20.0,
                    "offensive_rebounds": 7,
                    "outcome": Outcome.WIN,
                    "personal_fouls": 24,
                    "points": 114,
                    "steal_percentage": 13.8,
                    "steals": 14,
                    "team": Team.MINNESOTA_TIMBERWOLVES,
                    "three_point_attempt_rate": 0.247,
                    "total_rebound_percentage": 52.6,
                    "true_shooting_percentage": 0.605,
                    "turnover_rate": 15.3,
                    "turnovers": 17
                },
                {
                    "assist_percentage": 61.4,
                    "assists": 27,
                    "attempted_field_goals": 93,
                    "attempted_free_throws": 28,
                    "attempted_three_point_field_goals": 27,
                    "block_percentage": 5.2,
                    "blocks": 3,
                    "defensive_rating": 120.8,
                    "defensive_rebound_percentage": 84.6,
                    "defensive_rebounds": 33,
                    "effective_field_goal_percentage": 0.543,
                    "free_throw_attempt_rate": 0.301,
                    "made_field_goals": 44,
                    "made_free_throws": 26,
                    "made_three_point_field_goals": 13,
                    "minutes_played": 265,
                    "offensive_rating": 117.1,
                    "offensive_rebound_percentage": 22.7,
                    "offensive_rebounds": 10,
                    "outcome": Outcome.LOSS,
                    "personal_fouls": 23,
                    "points": 127,
                    "steal_percentage": 8.3,
                    "steals": 9,
                    "team": Team.MILWAUKEE_BUCKS,
                    "three_point_attempt_rate": 0.29,
                    "total_rebound_percentage": 51.8,
                    "true_shooting_percentage": 0.603,
                    "turnover_rate": 12.5,
                    "turnovers": 15
                },
                {
                    "assist_percentage": 55.6,
                    "assists": 25,
                    "attempted_field_goals": 91,
                    "attempted_free_throws": 33,
                    "attempted_three_point_field_goals": 33,
                    "block_percentage": 12.1,
                    "blocks": 8,
                    "defensive_rating": 117.1,
                    "defensive_rebound_percentage": 77.3,
                    "defensive_rebounds": 34,
                    "effective_field_goal_percentage": 0.571,
                    "free_throw_attempt_rate": 0.363,
                    "made_field_goals": 45,
                    "made_free_throws": 27,
                    "made_three_point_field_goals": 14,
                    "minutes_played": 265,
                    "offensive_rating": 120.8,
                    "offensive_rebound_percentage": 15.4,
                    "offensive_rebounds": 6,
                    "outcome": Outcome.WIN,
                    "personal_fouls": 20,
                    "points": 131,
                    "steal_percentage": 7.4,
                    "steals": 8,
                    "team": Team.TORONTO_RAPTORS,
                    "three_point_attempt_rate": 0.363,
                    "total_rebound_percentage": 48.2,
                    "true_shooting_percentage": 0.621,
                    "turnover_rate": 11.0,
                    "turnovers": 13
                }
            ]
        )


@BoxScoresResponseMocker(boxscore_date=date(year=2001, month=1, day=1))
class Test20010101TeamBoxScoresInMemoryOutput(TestCase):
    def test_output(self):
        team_box_scores = client.team_box_scores(day=1, month=1, year=2001)
        self.assertListEqual(
            team_box_scores,
            [
                {
                    "assist_percentage": 51.6,
                    "assists": 16,
                    "attempted_field_goals": 77,
                    "attempted_free_throws": 37,
                    "attempted_three_point_field_goals": 17,
                    "block_percentage": 4.1,
                    "blocks": 3,
                    "defensive_rating": 117.9,
                    "defensive_rebound_percentage": 70.3,
                    "defensive_rebounds": 26,
                    "effective_field_goal_percentage": 0.442,
                    "free_throw_attempt_rate": 0.481,
                    "made_field_goals": 31,
                    "made_free_throws": 28,
                    "made_three_point_field_goals": 6,
                    "minutes_played": 240,
                    "offensive_rating": 106.8,
                    "offensive_rebound_percentage": 21.7,
                    "offensive_rebounds": 10,
                    "outcome": Outcome.LOSS,
                    "personal_fouls": 19,
                    "points": 96,
                    "steal_percentage": 4.4,
                    "steals": 4,
                    "team": Team.HOUSTON_ROCKETS,
                    "three_point_attempt_rate": 0.221,
                    "total_rebound_percentage": 43.4,
                    "true_shooting_percentage": 0.515,
                    "turnover_rate": 10.5,
                    "turnovers": 11
                },
                {
                    "assist_percentage": 85.4,
                    "assists": 35,
                    "attempted_field_goals": 82,
                    "attempted_free_throws": 27,
                    "attempted_three_point_field_goals": 9,
                    "block_percentage": 3.3,
                    "blocks": 2,
                    "defensive_rating": 106.8,
                    "defensive_rebound_percentage": 78.3,
                    "defensive_rebounds": 36,
                    "effective_field_goal_percentage": 0.518,
                    "free_throw_attempt_rate": 0.329,
                    "made_field_goals": 41,
                    "made_free_throws": 21,
                    "made_three_point_field_goals": 3,
                    "minutes_played": 240,
                    "offensive_rating": 117.9,
                    "offensive_rebound_percentage": 29.7,
                    "offensive_rebounds": 11,
                    "outcome": Outcome.WIN,
                    "personal_fouls": 29,
                    "points": 106,
                    "steal_percentage": 6.7,
                    "steals": 6,
                    "team": Team.MINNESOTA_TIMBERWOLVES,
                    "three_point_attempt_rate": 0.11,
                    "total_rebound_percentage": 56.6,
                    "true_shooting_percentage": 0.565,
                    "turnover_rate": 7.9,
                    "turnovers": 8
                },
                {
                    "assist_percentage": 61.5,
                    "assists": 16,
                    "attempted_field_goals": 80,
                    "attempted_free_throws": 14,
                    "attempted_three_point_field_goals": 10,
                    "block_percentage": 1.8,
                    "blocks": 1,
                    "defensive_rating": 106.9,
                    "defensive_rebound_percentage": 70.3,
                    "defensive_rebounds": 26,
                    "effective_field_goal_percentage": 0.344,
                    "free_throw_attempt_rate": 0.175,
                    "made_field_goals": 26,
                    "made_free_throws": 12,
                    "made_three_point_field_goals": 3,
                    "minutes_played": 240,
                    "offensive_rating": 80.4,
                    "offensive_rebound_percentage": 29.4,
                    "offensive_rebounds": 15,
                    "outcome": Outcome.LOSS,
                    "personal_fouls": 25,
                    "points": 67,
                    "steal_percentage": 8.4,
                    "steals": 7,
                    "team": Team.CHARLOTTE_HORNETS,
                    "three_point_attempt_rate": 0.125,
                    "total_rebound_percentage": 46.6,
                    "true_shooting_percentage": 0.389,
                    "turnover_rate": 14.8,
                    "turnovers": 15
                },
                {
                    "assist_percentage": 69.0,
                    "assists": 20,
                    "attempted_field_goals": 70,
                    "attempted_free_throws": 30,
                    "attempted_three_point_field_goals": 15,
                    "block_percentage": 5.7,
                    "blocks": 4,
                    "defensive_rating": 80.4,
                    "defensive_rebound_percentage": 70.6,
                    "defensive_rebounds": 36,
                    "effective_field_goal_percentage": 0.443,
                    "free_throw_attempt_rate": 0.429,
                    "made_field_goals": 29,
                    "made_free_throws": 27,
                    "made_three_point_field_goals": 4,
                    "minutes_played": 240,
                    "offensive_rating": 106.9,
                    "offensive_rebound_percentage": 29.7,
                    "offensive_rebounds": 11,
                    "outcome": Outcome.WIN,
                    "personal_fouls": 17,
                    "points": 89,
                    "steal_percentage": 9.6,
                    "steals": 8,
                    "team": Team.PORTLAND_TRAIL_BLAZERS,
                    "three_point_attempt_rate": 0.214,
                    "total_rebound_percentage": 53.4,
                    "true_shooting_percentage": 0.535,
                    "turnover_rate": 14.4,
                    "turnovers": 14
                }
            ]
        )


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
class Test20180101TeamBoxScoresJSONOutput(TestCase):
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


@BoxScoresResponseMocker(boxscore_date=date(year=2001, month=1, day=1))
class Test20010101TeamBoxScoresJSONOutput(TestCase):
    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/team_box_scores/2001/01/01.json"
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/team_box_scores/2001/01/01.json"
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def test_output(self):
        client.team_box_scores(
            day=1,
            month=1,
            year=2001,
            output_type=OutputType.JSON,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE
        )
        self.assertTrue(
            filecmp.cmp(
                self.output_file_path,
                self.expected_output_file_path))
