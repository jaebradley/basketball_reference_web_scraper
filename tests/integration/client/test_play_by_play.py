import json
import os
from unittest import TestCase

import requests_mock

from basketball_reference_web_scraper.client import play_by_play
from basketball_reference_web_scraper.data import OutputType, OutputWriteOption, PeriodType
from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.errors import InvalidDate


class Test199911160ATLPlayByPlay(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/199911160ATL.html",
        ), 'r') as file_input: self._html = file_input.read();

    @requests_mock.Mocker()
    def test_length(self, m):
        m.get("https://www.basketball-reference.com/boxscores/pbp/199111160ATL.html", text=self._html, status_code=200)
        plays = play_by_play(home_team=Team.ATLANTA_HAWKS, day=16, month=11, year=1991)
        self.assertEqual(len(plays), 420)


class Test201810270MILPlayByPlay(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/201810270MIL.html",
        ), 'r') as file_input: self._html = file_input.read();

    @requests_mock.Mocker()
    def test_length(self, m):
        m.get('https://www.basketball-reference.com/boxscores/pbp/201810270MIL.html', text=self._html, status_code=200)
        plays = play_by_play(home_team=Team.MILWAUKEE_BUCKS, day=27, month=10, year=2018)
        self.assertEqual(len(plays), 465)

    @requests_mock.Mocker()
    def test_first_play(self, m):
        m.get('https://www.basketball-reference.com/boxscores/pbp/201810270MIL.html', text=self._html, status_code=200)
        plays = play_by_play(home_team=Team.MILWAUKEE_BUCKS, day=27, month=10, year=2018)
        self.assertEqual(
            plays[0],
            {
                "period": 1,
                "period_type": PeriodType.QUARTER,
                "relevant_team": Team.ORLANDO_MAGIC,
                "away_team": Team.ORLANDO_MAGIC,
                "home_team": Team.MILWAUKEE_BUCKS,
                "away_score": 0,
                "home_score": 0,
                "description": "N. Vučević misses 2-pt hook shot from 3 ft",
                "remaining_seconds_in_period": 703.0,
            }
        )

    @requests_mock.Mocker()
    def test_last_play(self, m):
        m.get('https://www.basketball-reference.com/boxscores/pbp/201810290MIL.html', text=self._html, status_code=200)
        plays = play_by_play(home_team=Team.MILWAUKEE_BUCKS, day=29, month=10, year=2018)
        self.assertEqual(
            plays[464],
            {
                "period": 4,
                "period_type": PeriodType.QUARTER,
                "relevant_team": Team.MILWAUKEE_BUCKS,
                "away_team": Team.ORLANDO_MAGIC,
                "home_team": Team.MILWAUKEE_BUCKS,
                "away_score": 91,
                "home_score": 113,
                "description": "Defensive rebound by T. Maker",
                "remaining_seconds_in_period": 2.0,
            })


class Test201901010DEN(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/201901010DEN.html",
        ), 'r') as file_input: self._html = file_input.read();

    @requests_mock.Mocker()
    def test_total_play_by_play_length_for_single_digit_month_and_day(self, m):
        m.get('https://www.basketball-reference.com/boxscores/pbp/201901010DEN.html', text=self._html, status_code=200)
        result = play_by_play(home_team=Team.DENVER_NUGGETS, day=1, month=1, year=2019)
        self.assertEqual(len(result), 464)

    @requests_mock.Mocker()
    def test_first_play_by_play_for_2019_01_01(self, m):
        m.get('https://www.basketball-reference.com/boxscores/pbp/201901010DEN.html', text=self._html, status_code=200)
        result = play_by_play(home_team=Team.DENVER_NUGGETS, day=1, month=1, year=2019)
        self.assertEqual(
            result[0],
            {
                "period": 1,
                "period_type": PeriodType.QUARTER,
                "relevant_team": Team.DENVER_NUGGETS,
                "away_team": Team.NEW_YORK_KNICKS,
                "home_team": Team.DENVER_NUGGETS,
                "away_score": 0,
                "home_score": 0,
                "description": "M. Plumlee misses 2-pt hook shot from 5 ft",
                "remaining_seconds_in_period": 693.0,
            }
        )

    @requests_mock.Mocker()
    def test_last_play_by_play_for_2019_01_01(self, m):
        m.get('https://www.basketball-reference.com/boxscores/pbp/201901010DEN.html', text=self._html, status_code=200)
        result = play_by_play(home_team=Team.DENVER_NUGGETS, day=1, month=1, year=2019)
        self.assertEqual(
            result[463],
            {
                "period": 4,
                "period_type": PeriodType.QUARTER,
                "relevant_team": Team.DENVER_NUGGETS,
                "away_team": Team.NEW_YORK_KNICKS,
                "home_team": Team.DENVER_NUGGETS,
                "away_score": 108,
                "home_score": 115,
                "description": "Defensive rebound by M. Beasley",
                "remaining_seconds_in_period": 12.0,
            }
        )


class Test201901010SAC(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/201901010SAC.html",
        ), 'r') as file_input: self._html = file_input.read();

    @requests_mock.Mocker()
    def test_last_play_by_play_for_overtime_game(self, m):
        m.get('https://www.basketball-reference.com/boxscores/pbp/201901010SAC.html', text=self._html, status_code=200)
        result = play_by_play(home_team=Team.SACRAMENTO_KINGS, day=1, month=1, year=2019)
        self.assertEqual(
            result[507],
            {
                "period": 1,
                "period_type": PeriodType.OVERTIME,
                "relevant_team": Team.PORTLAND_TRAIL_BLAZERS,
                "away_team": Team.PORTLAND_TRAIL_BLAZERS,
                "home_team": Team.SACRAMENTO_KINGS,
                "away_score": 113,
                "home_score": 108,
                "description": "Defensive rebound by J. Nurkić",
                "remaining_seconds_in_period": 3.0,
            }
        )


class Test201810160GSW(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/201810160GSW.html",
        ), 'r') as file_input: self._html = file_input.read();

    @requests_mock.Mocker()
    def test_non_unicode_matches(self, m):
        m.get('https://www.basketball-reference.com/boxscores/pbp/201810160GSW.html', text=self._html, status_code=200)
        plays = play_by_play(home_team=Team.GOLDEN_STATE_WARRIORS, day=16, month=10, year=2018)
        self.assertIsNotNone(plays)
        self.assertEqual(len(plays), 509)


class TestErrorCases(TestCase):

    @requests_mock.Mocker()
    def test_get_play_by_play_for_day_that_does_not_exist(self, m):
        m.get('https://www.basketball-reference.com/boxscores/pbp/201801-10MIL.html', text="Not found", status_code=404)
        self.assertRaisesRegex(
            InvalidDate,
            "Date with year set to 2018, month set to 1, and day set to -1 is invalid",
            play_by_play,
            home_team=Team.MILWAUKEE_BUCKS, day=-1, month=1, year=2018)


class TestPlayByPlayCSVOutput(TestCase):
    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/generated/2003_10_29_TOR_pbp.csv",
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2003_10_29_TOR_pbp.csv"
        )
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/200310290TOR.html",
        ), 'r') as file_input: self._html = file_input.read();

    def tearDown(self):
        os.remove(self.output_file_path)

    @requests_mock.Mocker()
    def test_play_by_play_output_for_200310290TOR(self, m):
        m.get('https://www.basketball-reference.com/boxscores/pbp/200310290TOR.html', text=self._html, status_code=200)
        play_by_play(
            home_team=Team.TORONTO_RAPTORS, day=29, month=10, year=2003,
            output_type=OutputType.CSV,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )
        with open(self.output_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(output_file.readlines(), expected_output_file.readlines())


class TestPlayByPlayJSONOutput(TestCase):
    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/generated/2003_10_29_TOR_pbp.json",
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2003_10_29_TOR_pbp.json"
        )
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/200310290TOR.html",
        ), 'r') as file_input: self._html = file_input.read();

    def tearDown(self):
        os.remove(self.output_file_path)

    @requests_mock.Mocker()
    def test_get_box_scores_from_2003_json(self, m):
        m.get('https://www.basketball-reference.com/boxscores/pbp/200310290TOR.html', text=self._html, status_code=200)
        play_by_play(
            home_team=Team.TORONTO_RAPTORS, day=29, month=10, year=2003,
            output_type=OutputType.JSON, output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )

        with open(self.output_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.load(output_file),
                json.load(expected_output_file),
            )
