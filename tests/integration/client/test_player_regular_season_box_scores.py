import json
import os
from datetime import datetime
from unittest import TestCase

import requests_mock

from basketball_reference_web_scraper.client import regular_season_player_box_scores
from basketball_reference_web_scraper.data import Team, Outcome, OutputType
from basketball_reference_web_scraper.errors import InvalidPlayerAndSeason


class TestWestbrook2020(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/player_box_scores/2020/westbru01.html"
        ), 'r') as file_input: self._html = file_input.read()

    @requests_mock.Mocker()
    def test_length(self, m):
        m.get("https://www.basketball-reference.com/players/w/westbru01/gamelog/2020",
              text=self._html,
              status_code=200)
        result = regular_season_player_box_scores(player_identifier="westbru01", season_end_year=2020)
        self.assertGreater(len(result), 0)

    @requests_mock.Mocker()
    def test_first_box_score(self, m):
        m.get("https://www.basketball-reference.com/players/w/westbru01/gamelog/2020",
              text=self._html,
              status_code=200)
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


class TestWestbrook2019(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/player_box_scores/2019/westbru01.html"
        ), 'r') as file_input: self._html = file_input.read()

    @requests_mock.Mocker()
    def test_length(self, m):
        m.get("https://www.basketball-reference.com/players/w/westbru01/gamelog/2019",
              text=self._html,
              status_code=200)
        result = regular_season_player_box_scores(player_identifier="westbru01", season_end_year=2019)
        self.assertEqual(len(result), 73)


class TestNonExistentPlayerPlayoffBoxScores(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/player_box_scores/2020/foobar.html"
        ), 'r') as file_input: self._html = file_input.read()

    @requests_mock.Mocker()
    def test_non_existent_player_raises(self, m):
        # bbref won't actually 404 or 500 if the player/season is invalid, it'll
        # just take you to the player page with blank data

        m.get("https://www.basketball-reference.com/players/f/foobar/gamelog/2020",
              text=self._html,
              status_code=200)

        self.assertRaisesRegex(
            InvalidPlayerAndSeason,
            'Player with identifier "foobar" in season ending in 2020 is invalid',
            regular_season_player_box_scores,
            player_identifier='foobar',
            season_end_year=2020,
        )


class TestJabariBrown2015(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/player_box_scores/2015/brownja01.html"
        ), 'r') as file_input: self._html = file_input.read()

    @requests_mock.Mocker()
    def test_default_does_not_include_inactive_games(self, m):
        m.get("https://www.basketball-reference.com/players/b/brownja01/gamelog/2015",
              text=self._html,
              status_code=200)

        # Jabari Brown was a DNP in his first game in the gamelog for the 2014-2015 season
        # https://www.basketball-reference.com/players/b/brownja01/gamelog/2015
        # The date for the DNP was 2015-03-10 while the first game he was active was on 2015-03-12
        # The first game that is returned should be on 2015-03-12
        results = regular_season_player_box_scores(player_identifier="brownja01", season_end_year=2015)
        self.assertEqual(19, len(results))
        self.assertEqual(datetime.strptime("2015-03-12", "%Y-%m-%d").date(), results[0]["date"])

    @requests_mock.Mocker()
    def test_does_not_include_inactive_games_when_explicitly_specified(self, m):
        m.get("https://www.basketball-reference.com/players/b/brownja01/gamelog/2015",
              text=self._html,
              status_code=200)

        # Jabari Brown was a DNP in his first game in the gamelog for the 2014-2015 season
        # https://www.basketball-reference.com/players/b/brownja01/gamelog/2015
        # The date for the DNP was 2015-03-10 while the first game he was active was on 2015-03-12
        # The first game that is returned should be on 2015-03-12
        results = regular_season_player_box_scores(player_identifier="brownja01", season_end_year=2015,
                                                   include_inactive_games=False)
        self.assertEqual(19, len(results))
        self.assertEqual(datetime.strptime("2015-03-12", "%Y-%m-%d").date(), results[0]["date"])

    @requests_mock.Mocker()
    def test_include_inactive_games_when_explicitly_specified(self, m):
        m.get("https://www.basketball-reference.com/players/b/brownja01/gamelog/2015",
              text=self._html,
              status_code=200)

        # Use Jabari Brown's 2014-2015 season again as we know it has one DNP
        results = regular_season_player_box_scores(player_identifier="brownja01", season_end_year=2015,
                                                   include_inactive_games=True)
        self.assertIsNotNone(results)
        self.assertEqual(20, len(results))

        inactive_game = results[0]
        self.assertEqual(datetime.strptime("2015-03-10", "%Y-%m-%d").date(), results[0]["date"])
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


class TestAveryBradley2019(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/player_box_scores/2019/bradlav01.html"
        ), 'r') as file_input: self._html = file_input.read()
        self.expected_excluding_inactive_games_output_json_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/player_box_scores/2019/bradlav01/exclude_inactive.json",
        )
        self.expected_excluding_inactive_games_output_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/player_box_scores/2019/bradlav01/exclude_inactive.csv",
        )
        self.expected_including_inactive_games_output_json_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/player_box_scores/2019/bradlav01/include_inactive.json",
        )
        self.expected_including_inactive_games_output_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/player_box_scores/2019/bradlav01/include_inactive.csv",
        )

    @requests_mock.Mocker()
    def test_in_memory_json_output(self, m):
        m.get("https://www.basketball-reference.com/players/b/bradlav01/gamelog/2019",
              text=self._html,
              status_code=200)

        results = regular_season_player_box_scores(
            player_identifier="bradlav01",
            season_end_year=2019,
            output_type=OutputType.JSON,
        )
        with open(self.expected_excluding_inactive_games_output_json_file_path, "r",
                  encoding="utf8") as expected_output:
            self.assertEqual(
                json.loads(results),
                json.load(expected_output),
            )

    @requests_mock.Mocker()
    def test_json_file_output_excluding_inactive_games(self, m):
        m.get("https://www.basketball-reference.com/players/b/bradlav01/gamelog/2019",
              text=self._html,
              status_code=200)

        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/player_box_scores/2019/bradlav01/exclude_inactive.json",
        )

        try:
            regular_season_player_box_scores(
                player_identifier="bradlav01",
                season_end_year=2019,
                output_type=OutputType.JSON,
                output_file_path=output_file_path,
            )
            with open(output_file_path, 'r', encoding="utf8") as output_file, \
                    open(self.expected_excluding_inactive_games_output_json_file_path, 'r',
                         encoding="utf8") as expected_file:
                output_lines = output_file.readlines()
                expected_lines = expected_file.readlines()

            self.assertEqual(output_lines, expected_lines)
        finally:
            os.remove(output_file_path)

    @requests_mock.Mocker()
    def test_json_output_including_inactive_games(self, m):
        m.get("https://www.basketball-reference.com/players/b/bradlav01/gamelog/2019",
              text=self._html,
              status_code=200)

        results = regular_season_player_box_scores(
            player_identifier="bradlav01",
            season_end_year=2019,
            output_type=OutputType.JSON,
            include_inactive_games=True,
        )
        # Bradley only has 81 reported games in 2019 due to a mid-season trade
        self.assertEqual(81, len(json.loads(results)))

        with open(self.expected_including_inactive_games_output_json_file_path, "r",
                  encoding="utf8") as expected_output:
            self.assertEqual(
                json.loads(results),
                json.load(expected_output),
            )

    @requests_mock.Mocker()
    def test_csv_file_output_excluding_inactive_games(self, m):
        m.get("https://www.basketball-reference.com/players/b/bradlav01/gamelog/2019",
              text=self._html,
              status_code=200)

        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/player_box_scores/2019/bradlav01/exclude_inactive.csv",
        )

        try:
            regular_season_player_box_scores(
                player_identifier="bradlav01",
                season_end_year=2019,
                output_type=OutputType.CSV,
                output_file_path=output_file_path,
            )
            with open(output_file_path, 'r', encoding="utf8") as output_file, \
                    open(self.expected_excluding_inactive_games_output_csv_file_path, 'r',
                         encoding="utf8") as expected_file:
                output_lines = output_file.readlines()
                expected_lines = expected_file.readlines()

            self.assertEqual(output_lines, expected_lines)
        finally:
            os.remove(output_file_path)

    @requests_mock.Mocker()
    def test_csv_file_output_including_inactive_games(self, m):
        m.get("https://www.basketball-reference.com/players/b/bradlav01/gamelog/2019",
              text=self._html,
              status_code=200)

        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/player_box_scores/2019/bradlav01/include_inactive.csv",
        )

        try:
            regular_season_player_box_scores(
                player_identifier="bradlav01",
                season_end_year=2019,
                output_type=OutputType.CSV,
                output_file_path=output_file_path,
                include_inactive_games=True
            )
            with open(output_file_path, 'r', encoding="utf8") as output_file, \
                    open(self.expected_including_inactive_games_output_csv_file_path, 'r',
                         encoding="utf8") as expected_file:
                output_lines = output_file.readlines()
                expected_lines = expected_file.readlines()

            self.assertEqual(output_lines, expected_lines)
        finally:
            os.remove(output_file_path)
