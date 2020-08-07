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
