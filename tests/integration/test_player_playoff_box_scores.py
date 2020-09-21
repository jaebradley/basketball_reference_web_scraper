import json
import os
from datetime import datetime
from unittest import TestCase

from basketball_reference_web_scraper.client import playoff_player_box_scores
from basketball_reference_web_scraper.data import Team, Outcome, OutputType
from basketball_reference_web_scraper.errors import InvalidPlayerAndSeason


class TestPlayerPlayoffBoxScores(TestCase):
    def test_get_2019_playoff_box_scores_for_russell_westbrook(self):
        result = playoff_player_box_scores(player_identifier="westbru01", season_end_year=2019)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 5)

    def test_get_first_2019_playoff_box_score_for_russell_westbrook(self):
        result = playoff_player_box_scores(player_identifier="westbru01", season_end_year=2019)
        self.assertEqual(True, result[0]["active"])
        self.assertEqual(datetime.strptime("2019-04-14", "%Y-%m-%d").date(), result[0]["date"])
        self.assertEqual(Team.OKLAHOMA_CITY_THUNDER, result[0]["team"])
        self.assertEqual(Outcome.LOSS, result[0]["outcome"])
        self.assertEqual(2263, result[0]["seconds_played"])
        self.assertEqual(Team.PORTLAND_TRAIL_BLAZERS, result[0]["opponent"])
        self.assertEqual(8, result[0]["made_field_goals"])
        self.assertEqual(17, result[0]["attempted_field_goals"])
        self.assertEqual(0, result[0]["made_three_point_field_goals"])
        self.assertEqual(4, result[0]["attempted_three_point_field_goals"])
        self.assertEqual(8, result[0]["made_free_throws"])
        self.assertEqual(8, result[0]["attempted_free_throws"])
        self.assertEqual(0, result[0]["offensive_rebounds"])
        self.assertEqual(10, result[0]["defensive_rebounds"])
        self.assertEqual(10, result[0]["assists"])
        self.assertEqual(0, result[0]["steals"])
        self.assertEqual(0, result[0]["blocks"])
        self.assertEqual(4, result[0]["turnovers"])
        self.assertEqual(4, result[0]["personal_fouls"])
        self.assertEqual(24, result[0]["points_scored"])
        self.assertEqual(19.7, result[0]["game_score"])
        self.assertEqual(-10, result[0]["plus_minus"])

    def test_get_season_box_scores_for_player_that_does_not_exist_raises_exception(self):
        self.assertRaisesRegex(
            InvalidPlayerAndSeason,
            'Player with identifier "Foo Bar" in season ending in 2020 is invalid',
            playoff_player_box_scores,
            player_identifier='Foo Bar',
            season_end_year=2020,
        )

    def test_get_season_box_scores_for_invalid_season_raises_exception(self):
        # bbref won't actually 404 or 500 if the season is invalid, it'll
        # just take you to the player page with blank data
        self.assertRaisesRegex(
            InvalidPlayerAndSeason,
            'Player with identifier "westbru01" in season ending in 1991 is invalid',
            playoff_player_box_scores,
            player_identifier='westbru01',
            season_end_year=1991,
        )

    def test_outputting_2019_playoff_box_scores_for_kawhi_leonard_as_json(self):
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/test-kawhi-playoffs-2019.json",
        )
        results = playoff_player_box_scores(
            player_identifier="leonaka01",
            season_end_year=2019,
            output_type=OutputType.JSON,
        )
        with open(expected_output_file_path, "r", encoding="utf8") as expected_output:
            self.assertEqual(
                json.loads(results),
                json.load(expected_output),
            )

    def test_outputting_2019_playoff_box_scores_for_kawhi_leonard_as_json_file(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/test-kawhi-playoffs-2019.json",
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/test-kawhi-playoffs-2019.json",
        )
        playoff_player_box_scores(
            player_identifier="leonaka01",
            season_end_year=2019,
            output_type=OutputType.JSON,
            output_file_path=output_file_path
        )
        with open(output_file_path, "r", encoding="utf8") as output_file, \
                open(expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.load(output_file),
                json.load(expected_output_file),
            )
        os.remove(output_file_path)

    def test_outputting_2019_playoff_box_scores_for_kawhi_leonard_as_csv(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/test-kawhi-playoffs-2019.csv",
        )
        expected_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/test-kawhi-playoffs-2019.csv"
        )
        playoff_player_box_scores(
            player_identifier="leonaka01",
            season_end_year=2019,
            output_type=OutputType.CSV,
            output_file_path=output_file_path,
        )
        with open(output_file_path, "r", encoding="utf8") as output_file, \
                open(expected_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                output_file.readlines(),
                expected_output_file.readlines(),
            )
        os.remove(output_file_path)

    def test_get_playoff_box_scores_removes_inactive_games_by_default(self):
        # Giannis missed one playoff game in 2020. Verify that the game from
        # 9/8/2020 is not included in his boxscores.
        results = playoff_player_box_scores(player_identifier="antetgi01", season_end_year=2020)
        self.assertIsNotNone(results)
        self.assertEqual(9, len(results))

        d = datetime.strptime("2020-09-08", "%Y-%m-%d").date()
        self.assertTrue(all([bs["date"] != d and bs["active"] for bs in results]))

    def test_get_playoff_box_scores_keeps_inactive_games_if_requested(self):
        results = playoff_player_box_scores(player_identifier="antetgi01", season_end_year=2020, include_inactive_games=True)
        self.assertIsNotNone(results)
        self.assertEqual(10, len(results))

        inactive_game = results[-1]
        self.assertEqual(datetime.strptime("2020-09-08", "%Y-%m-%d").date(), inactive_game["date"])
        self.assertFalse(inactive_game["active"])

        expected_null_stats = {
            "seconds_played",
            "made_field_goals",
            "attempted_field_goals",
            "made_three_point_field_goals",
            "attempted_three_point_field_goals",
            "made_free_throws",
            "attempted_free_throws",
            "offensive_rebounds",
            "defensive_rebounds",
            "assists",
            "steals",
            "blocks",
            "turnovers",
            "personal_fouls",
            "points_scored",
            "game_score",
            "plus_minus",
        }

        for stat in expected_null_stats:
            self.assertIsNone(inactive_game[stat])

    def test_outputting_2020_playoff_box_scores_for_russell_westbrook_with_inactive_games_as_json(self):
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/test-westbrook-playoffs-2020-include-inactive.json",
        )
        results = playoff_player_box_scores(
            player_identifier="westbru01",
            season_end_year=2020,
            output_type=OutputType.JSON,
            include_inactive_games=True,
        )
        with open(expected_output_file_path, "r", encoding="utf8") as expected_output:
            self.assertEqual(
                json.loads(results),
                json.load(expected_output),
            )

    def test_outputting_2020_playoff_box_scores_for_russell_westbrook_with_inactive_games_as_json_file(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/test-westbrook-playoffs-2020-include-inactive.json",
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/test-westbrook-playoffs-2020-include-inactive.json",
        )
        playoff_player_box_scores(
            player_identifier="westbru01",
            season_end_year=2020,
            output_type=OutputType.JSON,
            output_file_path=output_file_path,
            include_inactive_games=True,
        )
        with open(output_file_path, "r", encoding="utf8") as output_file, \
                open(expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.load(output_file),
                json.load(expected_output_file),
            )
        os.remove(output_file_path)

    def test_outputting_2020_playoff_box_scores_for_russell_westbrook_with_inactive_games_as_csv(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/test-westbrook-playoffs-2020-include-inactive.csv",
        )
        expected_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/test-westbrook-playoffs-2020-include-inactive.csv"
        )
        playoff_player_box_scores(
            player_identifier="westbru01",
            season_end_year=2020,
            output_type=OutputType.CSV,
            output_file_path=output_file_path,
            include_inactive_games=True,
        )
        with open(output_file_path, "r", encoding="utf8") as output_file, \
                open(expected_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                output_file.readlines(),
                expected_output_file.readlines(),
            )
        os.remove(output_file_path)
