import json
import os
from datetime import date
from unittest import TestCase

from basketball_reference_web_scraper.client import players_advanced_season_totals
from basketball_reference_web_scraper.data import OutputType, Team, Position
from basketball_reference_web_scraper.errors import InvalidSeason


class BaseTestPlayerAdvancedSeasonTotalsCSVOutput(TestCase):
    @property
    def year(self):
        raise NotImplementedError

    @property
    def include_combined_values(self):
        raise NotImplementedError

    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/player_advanced_season_totals_{year}.csv".format(year=self.year),
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/player_advanced_season_totals_{year}.csv".format(year=self.year),
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def assert_player_advanced_season_totals_csv(self):
        players_advanced_season_totals(
            season_end_year=self.year,
            output_type=OutputType.CSV,
            output_file_path=self.output_file_path,
            include_combined_values=self.include_combined_values,
        )

        with open(self.output_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                output_file.readlines(),
                expected_output_file.readlines(),
            )


class BaseTestPlayerAdvancedSeasonTotalsJSONOutput(TestCase):
    @property
    def year(self):
        raise NotImplementedError

    @property
    def include_combined_values(self):
        raise NotImplementedError

    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/player_advanced_season_totals_{year}.json".format(year=self.year),
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/player_advanced_season_totals_{year}.json".format(year=self.year),
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def assert_player_advanced_season_totals_json(self):
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


class TestPlayerAdvancedSeasonTotalsInMemoryOutput(TestCase):
    def test_future_season_raises_invalid_season(self):
        current_year = date.today().year
        future_year = current_year + 10
        expected_message = "Season end year of {future_year} is invalid".format(future_year=future_year)
        self.assertRaisesRegex(InvalidSeason, expected_message, players_advanced_season_totals, season_end_year=future_year)

    def test_2018_players_advanced_season_totals_length(self):
        result = players_advanced_season_totals(season_end_year=2018)
        self.assertEqual(len(result), 605)

    def test_first_2018_players_advanced_season_totals_row(self):
        result = players_advanced_season_totals(season_end_year=2018)
        self.assertEqual(
            result[0],
            {
                "age": 24,
                "assist_percentage": 3.4,
                "block_percentage": 0.6,
                "box_plus_minus": -1.5,
                "defensive_box_plus_minus": 0.4,
                "defensive_rebound_percentage": 8.9,
                "defensive_win_shares": 1.0,
                "free_throw_attempt_rate": 0.158,
                "games_played": 75,
                "is_combined_totals": False,
                "minutes_played": 1134,
                "name": "\u00c1lex Abrines",
                "offensive_box_plus_minus": -1.9,
                "offensive_rebound_percentage": 2.5,
                "offensive_win_shares": 1.3,
                "player_efficiency_rating": 9.0,
                "positions": [
                    Position.SHOOTING_GUARD,
                ],
                "slug": "abrinal01",
                "steal_percentage": 1.7,
                "team": Team.OKLAHOMA_CITY_THUNDER,
                "three_point_attempt_rate": 0.759,
                "total_rebound_percentage": 5.6,
                "true_shooting_percentage": 0.567,
                "turnover_percentage": 7.4,
                "usage_percentage": 12.7,
                "value_over_replacement_player": 0.1,
                "win_shares": 2.2,
                "win_shares_per_48_minutes": 0.094
            },
        )

    def test_last_2018_players_advanced_season_totals_row(self):
        result = players_advanced_season_totals(season_end_year=2018)
        self.assertEqual(
            result[604],
            {
                "age": 20,
                "assist_percentage": 8.8,
                "block_percentage": 3.0,
                "box_plus_minus": -2.0,
                "defensive_box_plus_minus": -0.3,
                "defensive_rebound_percentage": 20.1,
                "defensive_win_shares": 0.5,
                "free_throw_attempt_rate": 0.418,
                "games_played": 43,
                "is_combined_totals": False,
                "minutes_played": 410,
                "name": "Ivica Zubac",
                "offensive_box_plus_minus": -1.8,
                "offensive_rebound_percentage": 11.8,
                "offensive_win_shares": 0.5,
                "player_efficiency_rating": 15.3,
                "positions": [
                    Position.CENTER
                ],
                "slug": "zubaciv01",
                "steal_percentage": 0.9,
                "team": Team.LOS_ANGELES_LAKERS,
                "three_point_attempt_rate": 0.008,
                "total_rebound_percentage": 16.0,
                "true_shooting_percentage": 0.557,
                "turnover_percentage": 15.3,
                "usage_percentage": 17.6,
                "value_over_replacement_player": 0.0,
                "win_shares": 1.0,
                "win_shares_per_48_minutes": 0.118
            }
        )

    def test_players_advanced_season_totals_json(self):
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/player_advanced_season_totals_2018.json",
        )
        result = players_advanced_season_totals(season_end_year=2018, output_type=OutputType.JSON)
        with open(expected_output_file_path, "r", encoding="utf8") as expected_output:
            self.assertEqual(
                json.loads(result),
                json.load(expected_output),
            )
