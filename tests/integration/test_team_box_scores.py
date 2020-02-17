from unittest import TestCase
from unittest.mock import patch, MagicMock
import os

import requests
from requests.exceptions import HTTPError

import basketball_reference_web_scraper.client as client
from basketball_reference_web_scraper.data import OutputWriteOption, OutputType, Team, Outcome
from basketball_reference_web_scraper.errors import InvalidDate


class TestTeamBoxScores(TestCase):

    @patch('basketball_reference_web_scraper.http_client.team_box_scores')
    def test_invalid_date_error_raised_for_unknown_date(self, mocked_http_team_box_scores):
        mocked_http_team_box_scores.side_effect = HTTPError(
            response=MagicMock(status_code=requests.codes.not_found)
        )
        self.assertRaisesRegex(
            InvalidDate,
            "Date with year set to jae, month set to bae, and day set to bae is invalid",
            client.team_box_scores,
            day="bae",
            month="bae",
            year="jae"
        )

    def test_2018_01_01_team_box_scores(self):
        team_box_scores = client.team_box_scores(day=1, month=1, year=2018)
        self.assertIsNotNone(team_box_scores)

    def test_2001_01_01_team_box_scores(self):
        team_box_scores = client.team_box_scores(day=1, month=1, year=2001)
        self.assertIsNotNone(team_box_scores)

    def test_2004_01_02_team_box_scores(self):
        team_box_scores = client.team_box_scores(day=2, month=1, year=2004)
        self.assertIsNotNone(team_box_scores)

    def test_2018_01_01_team_box_scores_json_box_scores_to_file(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/2018_01_01_team_box_scores.json"
        )
        client.team_box_scores(
            day=1,
            month=1,
            year=2018,
            output_type=OutputType.JSON,
            output_file_path=output_file_path,
            output_write_option=OutputWriteOption.WRITE
        )

    def test_2018_01_01_team_box_scores_json_box_scores_to_memory(self):
        january_first_box_scores = client.team_box_scores(
            day=1,
            month=1,
            year=2018,
            output_type=OutputType.JSON,
        )

        self.assertIsNotNone(january_first_box_scores)

    def test_2018_01_01_team_box_scores_csv_box_scores_to_file(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/2018_01_01_team_box_scores.csv"
        )
        client.team_box_scores(
            day=1,
            month=1,
            year=2018,
            output_type=OutputType.CSV,
            output_file_path=output_file_path,
            output_write_option=OutputWriteOption.WRITE
        )

    def test_2019_10_22_has_four_team_box_scores(self):
        team_box_scores = client.team_box_scores(day=22, month=10, year=2019)
        self.assertEqual(4, len(team_box_scores))

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
