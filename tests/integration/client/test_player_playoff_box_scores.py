import filecmp
import json
import os
from datetime import datetime
from unittest import TestCase

import requests_mock

from basketball_reference_web_scraper.client import playoff_player_box_scores
from basketball_reference_web_scraper.data import Team, Outcome, OutputType
from basketball_reference_web_scraper.errors import InvalidPlayerAndSeason


class TestRussellWestbrook2019(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/playoff_player_box_scores/2019/westbru01.html"
        ), 'r') as file_input: self._html = file_input.read()

    @requests_mock.Mocker()
    def test_length(self, m):
        m.get("https://www.basketball-reference.com/players/w/westbru01/gamelog/2019",
              text=self._html,
              status_code=200)
        result = playoff_player_box_scores(player_identifier="westbru01", season_end_year=2019)
        self.assertEqual(len(result), 5)

    @requests_mock.Mocker()
    def test_first_game(self, m):
        m.get("https://www.basketball-reference.com/players/w/westbru01/gamelog/2019",
              text=self._html,
              status_code=200)
        result = playoff_player_box_scores(player_identifier="westbru01", season_end_year=2019)
        first_game = result[0]
        self.assertEqual(True, first_game["active"])
        self.assertEqual(datetime.strptime("2019-04-14", "%Y-%m-%d").date(), first_game["date"])
        self.assertEqual(Team.OKLAHOMA_CITY_THUNDER, first_game["team"])
        self.assertEqual(Outcome.LOSS, first_game["outcome"])
        self.assertEqual(2263, first_game["seconds_played"])
        self.assertEqual(Team.PORTLAND_TRAIL_BLAZERS, first_game["opponent"])
        self.assertEqual(8, first_game["made_field_goals"])
        self.assertEqual(17, first_game["attempted_field_goals"])
        self.assertEqual(0, first_game["made_three_point_field_goals"])
        self.assertEqual(4, first_game["attempted_three_point_field_goals"])
        self.assertEqual(8, first_game["made_free_throws"])
        self.assertEqual(8, first_game["attempted_free_throws"])
        self.assertEqual(0, first_game["offensive_rebounds"])
        self.assertEqual(10, first_game["defensive_rebounds"])
        self.assertEqual(10, first_game["assists"])
        self.assertEqual(0, first_game["steals"])
        self.assertEqual(0, first_game["blocks"])
        self.assertEqual(4, first_game["turnovers"])
        self.assertEqual(4, first_game["personal_fouls"])
        self.assertEqual(24, first_game["points_scored"])
        self.assertEqual(19.7, first_game["game_score"])
        self.assertEqual(-10, first_game["plus_minus"])


class RussellWestbrook2020IncludingInactiveGames(TestCase):

    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/playoff_player_box_scores/2020/westbru01.html"
        ), 'r') as file_input: self._html = file_input.read()
        self.expected_output_json_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/playoff_player_box_scores/2020/westbru01/include_inactive.json",
        )
        self.expected_output_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/playoff_player_box_scores/2020/westbru01/include_inactive.csv",
        )

    @requests_mock.Mocker()
    def test_in_memory_json_output(self, m):
        m.get("https://www.basketball-reference.com/players/w/westbru01/gamelog/2020",
              text=self._html,
              status_code=200)

        results = playoff_player_box_scores(
            player_identifier="westbru01",
            season_end_year=2020,
            output_type=OutputType.JSON,
            include_inactive_games=True,
        )
        with open(self.expected_output_json_file_path, "r", encoding="utf8") as expected_output:
            self.assertEqual(
                json.loads(results),
                json.load(expected_output),
            )

    @requests_mock.Mocker()
    def test_json_file_output(self, m):
        m.get("https://www.basketball-reference.com/players/w/westbru01/gamelog/2020",
              text=self._html,
              status_code=200)

        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/playoff_player_box_scores/2020/westbru01/include-include.json",
        )

        try:
            playoff_player_box_scores(
                player_identifier="westbru01",
                season_end_year=2020,
                output_type=OutputType.JSON,
                output_file_path=output_file_path,
                include_inactive_games=True,
            )
            self.assertTrue(
                filecmp.cmp(
                    output_file_path,
                    self.expected_output_json_file_path))
        finally:
            os.remove(output_file_path)

    @requests_mock.Mocker()
    def test_csv_file_output(self, m):
        m.get("https://www.basketball-reference.com/players/w/westbru01/gamelog/2020",
              text=self._html,
              status_code=200)

        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/playoff_player_box_scores/2020/westbru01/include-include.csv",
        )

        try:
            playoff_player_box_scores(
                player_identifier="westbru01",
                season_end_year=2020,
                output_type=OutputType.CSV,
                output_file_path=output_file_path,
                include_inactive_games=True,
            )
            self.assertTrue(
                filecmp.cmp(
                    output_file_path,
                    self.expected_output_csv_file_path))
        finally:
            os.remove(output_file_path)


class TestNonExistentPlayerPlayoffBoxScores(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/playoff_player_box_scores/2020/foobar.html"
        ), 'r') as file_input: self._html = file_input.read()

    @requests_mock.Mocker()
    def test_get_season_box_scores_for_player_that_does_not_exist_raises_exception(self, m):
        # bbref won't actually 404 or 500 if the player/season is invalid, it'll
        # just take you to the player page with blank data

        m.get("https://www.basketball-reference.com/players/f/foobar/gamelog/2020",
              text=self._html,
              status_code=200)

        self.assertRaisesRegex(
            InvalidPlayerAndSeason,
            'Player with identifier "foobar" in season ending in 2020 is invalid',
            playoff_player_box_scores,
            player_identifier='foobar',
            season_end_year=2020,
        )


class Giannis2020(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/playoff_player_box_scores/2020/antetgi01.html"
        ), 'r') as file_input: self._html = file_input.read()

    @requests_mock.Mocker()
    def test_inactive_games_are_removed_by_default(self, m):
        m.get("https://www.basketball-reference.com/players/a/antetgi01/gamelog/2020",
              text=self._html,
              status_code=200)
        # Giannis missed one playoff game in 2020. Verify that the game from
        # 9/8/2020 is not included in his boxscores.
        results = playoff_player_box_scores(player_identifier="antetgi01", season_end_year=2020)
        self.assertIsNotNone(results)
        self.assertEqual(9, len(results))

        d = datetime.strptime("2020-09-08", "%Y-%m-%d").date()
        self.assertTrue(all([bs["date"] != d and bs["active"] for bs in results]))

    @requests_mock.Mocker()
    def test_inactive_games_are_included_when_option_is_explicitly_selected(self, m):
        m.get("https://www.basketball-reference.com/players/a/antetgi01/gamelog/2020",
              text=self._html,
              status_code=200)
        results = playoff_player_box_scores(player_identifier="antetgi01", season_end_year=2020,
                                            include_inactive_games=True)
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
