import json
import os
from pathlib import Path
from unittest import TestCase

import basketball_reference_web_scraper.client as client
from basketball_reference_web_scraper.data import OutputWriteOption, OutputType, Team, Outcome


class TestTeamBoxScoresInMemoryOutput(TestCase):
    def test_2018_01_01_team_box_scores(self):
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
                    "turnovers": 14,
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
                    "turnovers": 12,
                    "personal_fouls": 20,
                    "points": 131,
                },
            ]
        )

    def test_2001_01_01_team_box_scores_with_charlotte_hornets(self):
        team_box_scores = client.team_box_scores(day=1, month=1, year=2001)
        self.assertListEqual(
            team_box_scores,
            [
                {
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
                },
                {
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
                },
                {
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
                },
                {
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
                }
            ])

    def test_2004_01_02_team_box_scores_with_new_orleans_hornets(self):
        team_box_scores = client.team_box_scores(day=11, month=12, year=2003)
        self.assertListEqual(
            team_box_scores,
            [
                {
                    "team": Team.DETROIT_PISTONS,
                    "outcome": Outcome.LOSS,
                    "minutes_played": 240,
                    "made_field_goals": 28,
                    "attempted_field_goals": 78,
                    "made_three_point_field_goals": 3,
                    "attempted_three_point_field_goals": 8,
                    "made_free_throws": 27,
                    "attempted_free_throws": 32,
                    "offensive_rebounds": 10,
                    "defensive_rebounds": 18,
                    "assists": 19,
                    "steals": 12,
                    "blocks": 2,
                    "turnovers": 14,
                    "personal_fouls": 25,
                    "points": 86,
                },
                {
                    "team": Team.CLEVELAND_CAVALIERS,
                    "outcome": Outcome.WIN,
                    "minutes_played": 240,
                    "made_field_goals": 35,
                    "attempted_field_goals": 66,
                    "made_three_point_field_goals": 2,
                    "attempted_three_point_field_goals": 5,
                    "made_free_throws": 23,
                    "attempted_free_throws": 30,
                    "offensive_rebounds": 10,
                    "defensive_rebounds": 35,
                    "assists": 25,
                    "steals": 6,
                    "blocks": 9,
                    "turnovers": 22,
                    "personal_fouls": 30,
                    "points": 95,
                },
                {
                    "team": Team.SAN_ANTONIO_SPURS,
                    "outcome": Outcome.WIN,
                    "minutes_played": 240,
                    "made_field_goals": 27,
                    "attempted_field_goals": 84,
                    "made_three_point_field_goals": 6,
                    "attempted_three_point_field_goals": 21,
                    "made_free_throws": 11,
                    "attempted_free_throws": 21,
                    "offensive_rebounds": 15,
                    "defensive_rebounds": 31,
                    "assists": 17,
                    "steals": 11,
                    "blocks": 6,
                    "turnovers": 12,
                    "personal_fouls": 13,
                    "points": 71,
                },
                {
                    "team": Team.HOUSTON_ROCKETS,
                    "outcome": Outcome.LOSS,
                    "minutes_played": 240,
                    "made_field_goals": 30,
                    "attempted_field_goals": 75,
                    "made_three_point_field_goals": 2,
                    "attempted_three_point_field_goals": 5,
                    "made_free_throws": 5,
                    "attempted_free_throws": 6,
                    "offensive_rebounds": 7,
                    "defensive_rebounds": 35,
                    "assists": 15,
                    "steals": 7,
                    "blocks": 8,
                    "turnovers": 20,
                    "personal_fouls": 24,
                    "points": 67,
                },
                {
                    "team": Team.NEW_ORLEANS_HORNETS,
                    "outcome": Outcome.WIN,
                    "minutes_played": 240,
                    "made_field_goals": 40,
                    "attempted_field_goals": 81,
                    "made_three_point_field_goals": 10,
                    "attempted_three_point_field_goals": 27,
                    "made_free_throws": 21,
                    "attempted_free_throws": 29,
                    "offensive_rebounds": 12,
                    "defensive_rebounds": 28,
                    "assists": 18,
                    "steals": 11,
                    "blocks": 3,
                    "turnovers": 16,
                    "personal_fouls": 17,
                    "points": 111,
                },
                {
                    "team": Team.PHOENIX_SUNS,
                    "outcome": Outcome.LOSS,
                    "minutes_played": 240,
                    "made_field_goals": 40,
                    "attempted_field_goals": 74,
                    "made_three_point_field_goals": 9,
                    "attempted_three_point_field_goals": 17,
                    "made_free_throws": 12,
                    "attempted_free_throws": 18,
                    "offensive_rebounds": 3,
                    "defensive_rebounds": 22,
                    "assists": 28,
                    "steals": 8,
                    "blocks": 1,
                    "turnovers": 13,
                    "personal_fouls": 23,
                    "points": 101,
                },
            ]
        )

    def test_2019_10_22_box_score_teams_and_outcomes(self):
        team_box_scores = client.team_box_scores(day=22, month=10, year=2019)
        lakers_box_score = team_box_scores[0]

        self.assertEqual(Team.LOS_ANGELES_LAKERS, lakers_box_score["team"])
        self.assertEqual(Outcome.LOSS, lakers_box_score["outcome"])
        self.assertEqual(102, lakers_box_score["points"])

        clippers_box_score = team_box_scores[1]

        self.assertEqual(Team.LOS_ANGELES_CLIPPERS, clippers_box_score["team"])
        self.assertEqual(Outcome.WIN, clippers_box_score["outcome"])
        self.assertEqual(112, clippers_box_score["points"])

        pelicans_box_score = team_box_scores[2]

        self.assertEqual(Team.NEW_ORLEANS_PELICANS, pelicans_box_score["team"])
        self.assertEqual(Outcome.LOSS, pelicans_box_score["outcome"])
        self.assertEqual(122, pelicans_box_score["points"])

        raptors_box_score = team_box_scores[3]

        self.assertEqual(Team.TORONTO_RAPTORS, raptors_box_score["team"])
        self.assertEqual(Outcome.WIN, raptors_box_score["outcome"])
        self.assertEqual(130, raptors_box_score["points"])


class TestTeamBoxScoresCSVOutput(TestCase):
    def setUp(self):
        self.file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/2018_01_01_team_box_scores.csv"
        )

    def tearDown(self):
        os.remove(self.file_path)

    def output_2018_01_01_team_box_scores_to_csv(self):
        client.team_box_scores(
            day=1,
            month=1,
            year=2018,
            output_type=OutputType.CSV,
            output_file_path=self.file_path,
            output_write_option=OutputWriteOption.WRITE
        )

    def test_2018_01_01_team_box_scores_csv_box_scores_to_file(self):
        self.output_2018_01_01_team_box_scores_to_csv()
        self.assertTrue(Path(self.file_path).exists())
        self.assertTrue(Path(self.file_path).is_file())

    def test_2019_01_01_team_box_scores_csv_values(self):
        self.output_2018_01_01_team_box_scores_to_csv()
        expected_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2018_01_01_team_box_scores.csv"
        )
        with open(self.file_path, 'r', encoding="utf8") as output_file, open(expected_file_path, 'r', encoding="utf8") as expected_file:
            output_lines = output_file.readlines()
            expected_lines = expected_file.readlines()

        self.assertEqual(output_lines, expected_lines)


class TestTeamBoxScoresInMemoryJSON(TestCase):
    def setUp(self):
        self.expected_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2018_01_01_team_box_scores.json"
        )

    def test_2018_01_01_team_box_scores_json_box_scores_to_memory(self):
        january_first_box_scores = client.team_box_scores(
            day=1,
            month=1,
            year=2018,
            output_type=OutputType.JSON,
        )
        with open(self.expected_file_path, encoding="utf8") as expected_json:
            self.assertEqual(json.loads(january_first_box_scores), json.load(expected_json))


class TestTeamBoxScoresJSONOutput(TestCase):
    def setUp(self):
        self.file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/2018_01_01_team_box_scores.json"
        )
        self.expected_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2018_01_01_team_box_scores.json"
        )

    def tearDown(self):
        os.remove(self.file_path)

    def test_2018_01_01_team_box_scores_json_box_scores_output_to_file(self):
        client.team_box_scores(
            day=1,
            month=1,
            year=2018,
            output_type=OutputType.JSON,
            output_file_path=self.file_path,
            output_write_option=OutputWriteOption.WRITE
        )
        self.assertTrue(Path(self.file_path).exists())
        self.assertTrue(Path(self.file_path).is_file())

    def test_2018_01_01_team_box_scores_json_box_scores_match_expected_output(self):
        client.team_box_scores(
            day=1,
            month=1,
            year=2018,
            output_type=OutputType.JSON,
            output_file_path=self.file_path,
            output_write_option=OutputWriteOption.WRITE
        )

        with open(self.file_path, 'r', encoding="utf8") as output_file, open(self.expected_file_path, 'r', encoding="utf8") as expected_file:
            self.assertEqual(
                json.load(output_file),
                json.load(expected_file),
            )
