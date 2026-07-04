import filecmp
import json
import os
import sys
from unittest import TestCase

import requests_mock

from basketball_reference_web_scraper.client import players_advanced_season_totals
from basketball_reference_web_scraper.data import OutputType, Team, Position
from basketball_reference_web_scraper.errors import InvalidSeason


class Test2019(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/player_advanced_season_totals/2019.html",
        ), 'r') as file_input: self._html = file_input.read();

    @requests_mock.Mocker()
    def test_length(self, m):
        m.get("https://www.basketball-reference.com/leagues/NBA_2019_advanced.html", text=self._html, status_code=200)
        result = players_advanced_season_totals(season_end_year=2019)
        self.assertEqual(len(result), 622)


class BaseTestPlayerAdvancedSeasonTotalsCSVOutput(TestCase):
    @property
    def year(self):
        raise NotImplementedError

    @property
    def include_combined_values(self):
        raise NotImplementedError

    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                f"../files/player_advanced_season_totals/{self.year}.html",
        ), 'r') as file_input: self._html = file_input.read()

        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            f"./output/generated/player_advanced_season_totals/{self.year}.csv",
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            f"./output/expected/player_advanced_season_totals/{self.year}.csv",
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    @requests_mock.Mocker()
    def assert_player_advanced_season_totals_csv(self, m):
        m.get(f"https://www.basketball-reference.com/leagues/NBA_{self.year}_advanced.html",
              text=self._html,
              status_code=200)

        players_advanced_season_totals(
            season_end_year=self.year,
            output_type=OutputType.CSV,
            output_file_path=self.output_file_path,
            include_combined_values=self.include_combined_values,
        )

        self.assertTrue(
            filecmp.cmp(
                self.output_file_path,
                self.expected_output_file_path))


class BaseTestPlayerAdvancedSeasonTotalsJSONOutput(TestCase):
    @property
    def year(self):
        raise NotImplementedError

    @property
    def include_combined_values(self):
        raise NotImplementedError

    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                f"../files/player_advanced_season_totals/{self.year}.html",
        ), 'r') as file_input: self._html = file_input.read()

        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            f"./output/generated/player_advanced_season_totals/{self.year}.json",
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            f"./output/expected/player_advanced_season_totals/{self.year}.json",
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    @requests_mock.Mocker()
    def assert_player_advanced_season_totals_json(self, m):
        m.get(f"https://www.basketball-reference.com/leagues/NBA_{self.year}_advanced.html",
              text=self._html,
              status_code=200)

        players_advanced_season_totals(
            season_end_year=self.year,
            output_type=OutputType.JSON,
            output_file_path=self.output_file_path,
            include_combined_values=self.include_combined_values,
        )

        with open(self.output_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.load(output_file),
                json.load(expected_output_file),
            )


class Test2019PlayerAdvancedSeasonTotalsCSVOutput(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2019

    @property
    def include_combined_values(self):
        return False

    def test_players_advanced_season_totals_csv(self):
        self.assert_player_advanced_season_totals_csv()


class Test2018PlayerAdvancedSeasonTotalsCSVOutput(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2018

    @property
    def include_combined_values(self):
        return False

    def test_players_advanced_season_totals_csv(self):
        self.assert_player_advanced_season_totals_csv()


class Test2017PlayerAdvancedSeasonTotalsCSVOutput(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2017

    @property
    def include_combined_values(self):
        return True

    def test_players_advanced_season_totals_csv(self):
        self.assert_player_advanced_season_totals_csv()


class Test2016PlayerAdvancedSeasonTotalsCSVOutput(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2016

    @property
    def include_combined_values(self):
        return True

    def test_players_advanced_season_totals_csv(self):
        self.assert_player_advanced_season_totals_csv()


class Test2001PlayerAdvancedSeasonTotalsCSVOutput(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2001

    @property
    def include_combined_values(self):
        return False

    def test_players_advanced_season_totals_csv(self):
        self.assert_player_advanced_season_totals_csv()


class Test2019PlayerAdvancedSeasonTotalsJSONOutput(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2019

    @property
    def include_combined_values(self):
        return False

    def test_players_advanced_season_totals_json(self):
        self.assert_player_advanced_season_totals_json()


class Test2018PlayerAdvancedSeasonTotalsJSONOutput(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2018

    @property
    def include_combined_values(self):
        return False

    def test_players_advanced_season_totals_json(self):
        self.assert_player_advanced_season_totals_json()


class Test2017PlayerAdvancedSeasonTotalsJSONOutput(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2017

    @property
    def include_combined_values(self):
        return True

    def test_players_advanced_season_totals_json(self):
        self.assert_player_advanced_season_totals_json()


class Test2016PlayerAdvancedSeasonTotalsJSONOutput(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2016

    @property
    def include_combined_values(self):
        return True

    def test_players_advanced_season_totals_json(self):
        self.assert_player_advanced_season_totals_json()


class Test2001PlayerAdvancedSeasonTotalsJSONOutput(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2001

    @property
    def include_combined_values(self):
        return False

    def test_players_advanced_season_totals_json(self):
        self.assert_player_advanced_season_totals_json()


@requests_mock.Mocker()
class TestPlayerAdvancedSeasonTotalsInMemoryOutput(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                f"../files/player_advanced_season_totals/2018.html",
        ), 'r') as file_input: self._html = file_input.read()

    def test_future_season_raises_invalid_season(self, m):
        m.get(f"https://www.basketball-reference.com/leagues/NBA_{sys.maxsize}_advanced.html",
              text="Not found",
              status_code=404)
        self.assertRaisesRegex(InvalidSeason, f"Season end year of {sys.maxsize} is invalid",
                               players_advanced_season_totals,
                               season_end_year=sys.maxsize)

    def test_2018_players_advanced_season_totals_length(self, m):
        m.get(f"https://www.basketball-reference.com/leagues/NBA_2018_advanced.html",
              text=self._html,
              status_code=200)

        result = players_advanced_season_totals(season_end_year=2018)
        self.assertEqual(len(result), 605)

    def test_first_2018_players_advanced_season_totals_row(self, m):
        m.get(f"https://www.basketball-reference.com/leagues/NBA_2018_advanced.html",
              text=self._html,
              status_code=200)

        result = players_advanced_season_totals(season_end_year=2018)
        self.assertEqual(
            result[0],
            {
                "age": 33,
                "assist_percentage": 44.4,
                "block_percentage": 2.0,
                "box_plus_minus": 8.7,
                "defensive_box_plus_minus": 1.4,
                "defensive_rebound_percentage": 22.3,
                "defensive_win_shares": 3.0,
                "free_throw_attempt_rate": 0.336,
                "games_played": 82,
                "is_combined_totals": False,
                "minutes_played": 3026,
                "name": "LeBron James",
                "offensive_box_plus_minus": 7.3,
                "offensive_rebound_percentage": 3.7,
                "offensive_win_shares": 11.0,
                "player_efficiency_rating": 28.6,
                "positions": [
                    Position.POWER_FORWARD,
                ],
                "slug": "jamesle01",
                "steal_percentage": 1.9,
                "team": Team.CLEVELAND_CAVALIERS,
                "three_point_attempt_rate": 0.257,
                "total_rebound_percentage": 13.1,
                "true_shooting_percentage": 0.621,
                "turnover_percentage": 16.1,
                "usage_percentage": 31.6,
                "value_over_replacement_player": 8.2,
                "win_shares": 14.0,
                "win_shares_per_48_minutes": 0.221
            },
        )

    def test_last_2018_players_advanced_season_totals_row(self, m):
        m.get(f"https://www.basketball-reference.com/leagues/NBA_2018_advanced.html",
              text=self._html,
              status_code=200)

        result = players_advanced_season_totals(season_end_year=2018)
        self.assertEqual(
            result[604],
            {
                "age": 27,
                "assist_percentage": 0.0,
                "block_percentage": 0.0,
                "box_plus_minus": -8.5,
                "defensive_box_plus_minus": -2.3,
                "defensive_rebound_percentage": 0.0,
                "defensive_win_shares": 0.0,
                "free_throw_attempt_rate": 0.0,
                "games_played": 1,
                "is_combined_totals": False,
                "minutes_played": 1,
                "name": "Trey McKinney-Jones",
                "offensive_box_plus_minus": -6.2,
                "offensive_rebound_percentage": 0.0,
                "offensive_win_shares": 0.0,
                "player_efficiency_rating": 0.0,
                "positions": [
                    Position.SHOOTING_GUARD
                ],
                "slug": "mckintr01",
                "steal_percentage": 0.0,
                "team": Team.INDIANA_PACERS,
                "three_point_attempt_rate": 0.0,
                "total_rebound_percentage": 0.0,
                "true_shooting_percentage": 0.0,
                "turnover_percentage": 0.0,
                "usage_percentage": 0.0,
                "value_over_replacement_player": 0.0,
                "win_shares": 0.0,
                "win_shares_per_48_minutes": -0.001
            }
        )

    def test_players_advanced_season_totals_json(self, m):
        m.get(f"https://www.basketball-reference.com/leagues/NBA_2018_advanced.html",
              text=self._html,
              status_code=200)

        expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/player_advanced_season_totals/2018.json",
        )
        result = players_advanced_season_totals(season_end_year=2018, output_type=OutputType.JSON)
        with open(expected_output_file_path, "r", encoding="utf8") as expected_output:
            self.assertEqual(
                json.loads(result),
                json.load(expected_output),
            )
