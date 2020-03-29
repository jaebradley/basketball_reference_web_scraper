import json
import os
from datetime import datetime
from unittest import TestCase

from basketball_reference_web_scraper.client import regular_season_player_box_scores
from basketball_reference_web_scraper.data import Team, Outcome, OutputType
from basketball_reference_web_scraper.errors import InvalidPlayerAndSeason


class TestPlayerRegularSeasonBoxScores(TestCase):
    def test_get_2020_regular_season_box_scores_for_russell_westbrook(self):
        result = regular_season_player_box_scores(player_identifier="westbru01", season_end_year=2020)
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)

    def test_get_2019_regular_season_box_scores_for_russell_westbrook(self):
        result = regular_season_player_box_scores(player_identifier="westbru01", season_end_year=2019)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 73)

    def test_get_first_20202_regular_season_box_score_for_russell_westbrook(self):
        result = regular_season_player_box_scores(player_identifier="westbru01", season_end_year=2020)
        self.assertEqual(datetime.strptime("2019-10-24", "%Y-%m-%d").date(), result[0]["date"])
        self.assertEqual(Team.HOUSTON_ROCKETS, result[0]["team"])
        self.assertEqual(Outcome.LOSS, result[0]["outcome"])
        self.assertEqual(1972, result[0]["seconds_played"])
        self.assertEqual(Team.MILWAUKEE_BUCKS, result[0]["opponent"])
        self.assertEqual(7, result[0]["made_field_goals"])
        self.assertEqual(17, result[0]["attempted_field_goals"])
        self.assertEqual(3, result[0]["made_three_point_field_goals"])
        self.assertEqual(7, result[0]["attempted_three_point_field_goals"])
        self.assertEqual(7, result[0]["made_free_throws"])
        self.assertEqual(11, result[0]["attempted_free_throws"])
        self.assertEqual(4, result[0]["offensive_rebounds"])
        self.assertEqual(12, result[0]["defensive_rebounds"])
        self.assertEqual(7, result[0]["assists"])
        self.assertEqual(2, result[0]["steals"])
        self.assertEqual(1, result[0]["blocks"])
        self.assertEqual(3, result[0]["turnovers"])
        self.assertEqual(3, result[0]["personal_fouls"])
        self.assertEqual(24, result[0]["points_scored"])
        self.assertEqual(23.1, result[0]["game_score"])
        self.assertEqual(0, result[0]["plus_minus"])

    def test_get_season_box_scores_for_player_that_does_not_exist_raises_exception(self):
        self.assertRaisesRegex(
            InvalidPlayerAndSeason,
            'Player with identifier "Foo Bar" in season ending in 2020 is invalid',
            regular_season_player_box_scores,
            player_identifier='Foo Bar',
            season_end_year=2020,
        )

    def test_get_season_box_scores_for_invalid_season_raises_exception(self):
        # bbref won't actually 404 or 500 if the season is invalid, it'll
        # just take you to the player page with blank data
        self.assertRaisesRegex(
            InvalidPlayerAndSeason,
            'Player with identifier "westbru01" in season ending in 1991 is invalid',
            regular_season_player_box_scores,
            player_identifier='westbru01',
            season_end_year=1991,
        )

    def test_get_season_box_scores_removes_games_that_player_did_not_participate_in(self):
        # Jabari Brown was a DNP in his first game in the gamelog for the 2014-2015 season
        # https://www.basketball-reference.com/players/b/brownja01/gamelog/2015
        # The date for the DNP was 2015-03-10 while the first game he was active was on 2015-03-12
        # The first game that is returned should be on 2015-03-12
        results = regular_season_player_box_scores(player_identifier="brownja01", season_end_year=2015)
        self.assertIsNotNone(results)
        self.assertEqual(19, len(results))
        self.assertEqual(datetime.strptime("2015-03-12", "%Y-%m-%d").date(), results[0]["date"])

    def test_outputting_2019_regular_season_box_scores_for_avery_bradley_as_json(self):
        results = regular_season_player_box_scores(
            player_identifier="bradlav01",
            season_end_year=2019,
            output_type=OutputType.JSON,
        )
        self.assertIsNotNone(results)
        self.assertEqual(63, len(json.loads(results)))

    def test_outputting_2019_regular_season_box_scores_for_avery_bradley_as_csv(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/test-avery-2019.csv",
        )
        regular_season_player_box_scores(
            player_identifier="bradlav01",
            season_end_year=2019,
            output_type=OutputType.CSV,
            output_file_path=output_file_path,
        )
