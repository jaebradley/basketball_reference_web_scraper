import datetime
import filecmp
import os
import time
from unittest import TestCase

from basketball_reference_web_scraper.client import player_box_scores, season_schedule, players_advanced_season_totals, \
    play_by_play, players_season_totals, players_regular_season_shooting_statistics, roster, player_contracts
from basketball_reference_web_scraper.data import Location, Outcome
from basketball_reference_web_scraper.data import OutputWriteOption, OutputType, Team, PeriodType
from contracts.data.models import Player


class BaseEndToEndTest(TestCase):

    def setUp(self):
        # To avoid getting rate-limited
        time.sleep(20)

    def tearDown(self):
        # To avoid getting rate-limited
        time.sleep(20)


class TestPlayerBoxScores(BaseEndToEndTest):

    def setUp(self):
        super().setUp()

        self.box_scores = player_box_scores(day=11, month=3, year=2024)

    def test_first_entry(self):
        self.assertIsNotNone(self.box_scores)
        self.assertNotEqual(0, len(self.box_scores))
        self.assertEqual(124, len(self.box_scores))
        self.assertDictEqual({
            "name": "Nikola Jokić",
            "slug": "jokicni01",
            "team": Team.DENVER_NUGGETS,
            "opponent": Team.TORONTO_RAPTORS,
            "location": Location.HOME,
            "outcome": Outcome.WIN,
            "seconds_played": 2286,
            "made_field_goals": 14,
            "attempted_field_goals": 26,
            "made_three_point_field_goals": 1,
            "attempted_three_point_field_goals": 3,
            "made_free_throws": 6,
            "attempted_free_throws": 6,
            "offensive_rebounds": 6,
            "defensive_rebounds": 11,
            "assists": 12,
            "steals": 6,
            "blocks": 2,
            "turnovers": 2,
            "personal_fouls": 3,
            "plus_minus": 13.0,
            "game_score": 42.5,
        },
            self.box_scores[0])


class TestCsvPlayerBoxScores(BaseEndToEndTest):

    def test_csv_output(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/playerboxscores/2024/03/11.csv",
        )
        player_box_scores(
            day=11,
            month=3,
            year=2024,
            output_type=OutputType.CSV,
            output_file_path=output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )

        self.assertTrue(
            filecmp.cmp(
                output_file_path,
                os.path.join(
                    os.path.dirname(__file__),
                    "./output/expected/playerboxscores/2024/03/11.csv",
                )))


class TestJsonPlayerBoxScores(BaseEndToEndTest):

    def test_json_output(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/playerboxscores/2024/03/11.json",
        )
        player_box_scores(
            day=11,
            month=3,
            year=2024,
            output_type=OutputType.JSON,
            output_file_path=output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )

        self.assertTrue(
            filecmp.cmp(
                output_file_path,
                os.path.join(
                    os.path.dirname(__file__),
                    "./output/expected/playerboxscores/2024/03/11.json",
                )))


class TestSeasonSchedule(BaseEndToEndTest):
    def test_2001_season_schedule(self):
        schedule = season_schedule(season_end_year=2001)
        self.assertIsNotNone(schedule)

    def test_current_year_season_schedule(self):
        schedule = season_schedule(season_end_year=datetime.datetime.now().year)
        self.assertIsNotNone(schedule)


class TestPlayerAdvancedSeasonTotals(BaseEndToEndTest):
    def test_totals(self):
        player_season_totals = players_advanced_season_totals(season_end_year=2019)
        self.assertIsNotNone(player_season_totals)
        self.assertTrue(len(player_season_totals) > 0)


class TestPlayByPlay(BaseEndToEndTest):
    def test_BOS_2018_10_16_play_by_play(self):
        plays = play_by_play(
            home_team=Team.BOSTON_CELTICS,
            day=16,
            month=10,
            year=2018,
        )
        self.assertIsNotNone(plays)

    def test_BOS_2018_10_16_play_by_play_csv_to_file(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/2018_10_16_BOS_pbp.csv",
        )
        play_by_play(
            home_team=Team.BOSTON_CELTICS,
            day=16,
            month=10,
            year=2018,
            output_type=OutputType.CSV,
            output_file_path=output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )

        self.assertTrue(
            filecmp.cmp(
                output_file_path,
                os.path.join(
                    os.path.dirname(__file__),
                    "./output/expected/2018_10_16_BOS_pbp.csv",
                )))

    def test_overtime_play_by_play(self):
        plays = play_by_play(
            home_team=Team.PORTLAND_TRAIL_BLAZERS,
            day=22,
            month=10,
            year=2018,
        )
        last_play = plays[-1]
        self.assertIsNotNone(last_play)
        self.assertEqual(1, last_play["period"])
        self.assertEqual(PeriodType.OVERTIME, last_play["period_type"])

    def test_overtime_play_by_play_to_json_file(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/2018_10_22_POR_pbp.json",
        )
        play_by_play(
            home_team=Team.PORTLAND_TRAIL_BLAZERS,
            day=22,
            month=10,
            year=2018,
            output_type=OutputType.JSON,
            output_file_path=output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )

        self.assertTrue(
            filecmp.cmp(output_file_path,
                        os.path.join(
                            os.path.dirname(__file__),
                            "./output/expected/2018_10_22_POR_pbp.json",
                        )))


class TestPlayersSeasonTotals(BaseEndToEndTest):

    def test_2018(self):
        totals = players_season_totals(season_end_year=2018)

        for total in totals:
            # TODO: @jaebradley turn this into a dataclass with validation
            self.assertIsNot("", total["name"])
            self.assertIsNot("League Average", total["name"])
            self.assertTrue(total["slug"])
            self.assertTrue(total["name"])
            self.assertTrue(total["positions"])
            self.assertGreater(total["age"], 0)
            self.assertGreaterEqual(total["games_played"], 0)
            self.assertGreaterEqual(total["games_started"], 0)
            self.assertGreaterEqual(total["minutes_played"], 0)
            self.assertGreaterEqual(total["made_field_goals"], 0)
            self.assertGreaterEqual(total["attempted_field_goals"], total["made_field_goals"])
            self.assertGreaterEqual(total["made_three_point_field_goals"], 0)
            self.assertGreaterEqual(total["attempted_three_point_field_goals"], total["made_three_point_field_goals"])
            self.assertGreaterEqual(total["made_free_throws"], 0)
            self.assertGreaterEqual(total["attempted_free_throws"], total["made_free_throws"])
            self.assertGreaterEqual(total["offensive_rebounds"], 0)
            self.assertGreaterEqual(total["defensive_rebounds"], 0)
            self.assertGreaterEqual(total["assists"], 0)
            self.assertGreaterEqual(total["steals"], 0)
            self.assertGreaterEqual(total["blocks"], 0)
            self.assertGreaterEqual(total["turnovers"], 0)
            self.assertGreaterEqual(total["personal_fouls"], 0)
            self.assertGreaterEqual(total["points"], 0)


class TestPlayersRegularSeasonShootingStatistics(BaseEndToEndTest):
    def test_2026(self):
        totals = players_regular_season_shooting_statistics(season_end_year=2026)

        for total in totals:
            self.assertEqual(total.keys(), {"slug", "name", "position", "age", "team", "games_played", "games_started",
                                            "minutes_played", "field_goal_percentage",
                                            "average_field_goal_attempt_distance", "two_point_shot_statistics",
                                            "three_point_shot_statistics"})
            self.assertIsNot("", total["name"])
            self.assertIsNot("League Average", total["name"])
            self.assertTrue(total["slug"])
            self.assertTrue(total["name"])
            self.assertTrue(total["position"])
            self.assertGreater(total["age"], 0)
            self.assertGreaterEqual(total["games_played"], 0)
            self.assertGreaterEqual(total["games_started"], 0)
            self.assertGreaterEqual(total["minutes_played"], 0)
            self.assertIsNotNone(total["average_field_goal_attempt_distance"])
            self.assertGreaterEqual(total["average_field_goal_attempt_distance"]["value"], 0)
            self.assertEqual(total["average_field_goal_attempt_distance"]["units"], "feet")
            self.assertIsNotNone(total["two_point_shot_statistics"])
            self.assertGreaterEqual(total["two_point_shot_statistics"]["field_goal_percentage"], 0)
            self.assertLessEqual(total["two_point_shot_statistics"]["field_goal_percentage"], 1)
            self.assertGreaterEqual(total["two_point_shot_statistics"]["assisted_percentage"], 0)
            self.assertLessEqual(total["two_point_shot_statistics"]["assisted_percentage"], 1)
            self.assertGreaterEqual(total["two_point_shot_statistics"]["percentage_of_total_field_goal_attempts"], 0)
            self.assertLessEqual(total["two_point_shot_statistics"]["percentage_of_total_field_goal_attempts"], 1)
            self.assertIsNotNone(total["two_point_shot_statistics"]["statistics_by_range"])

            self.assertEqual(total["two_point_shot_statistics"]["statistics_by_range"].keys(),
                             {"0-3", "3-10", "10-16", "16+"})

            for key, range_statistics in total["two_point_shot_statistics"]["statistics_by_range"].items():
                self.assertEqual(range_statistics.keys(),
                                 {"percentage_of_total_field_goal_attempts", "field_goal_percentage", "units"}),
                self.assertGreaterEqual(range_statistics["percentage_of_total_field_goal_attempts"], 0)
                self.assertLessEqual(range_statistics["percentage_of_total_field_goal_attempts"], 1)
                self.assertGreaterEqual(range_statistics["field_goal_percentage"], 0)
                self.assertLessEqual(range_statistics["field_goal_percentage"], 1)
                self.assertEqual(range_statistics["units"], "feet")

            self.assertIsNotNone(total["two_point_shot_statistics"]["dunks"])
            self.assertEqual(total["two_point_shot_statistics"]["dunks"].keys(),
                             {"percentage_of_total_field_goal_attempts", "made"})
            self.assertGreaterEqual(total["two_point_shot_statistics"]["dunks"]["made"], 0)
            self.assertGreaterEqual(
                total["two_point_shot_statistics"]["dunks"]["percentage_of_total_field_goal_attempts"], 0)
            self.assertLessEqual(
                total["two_point_shot_statistics"]["dunks"]["percentage_of_total_field_goal_attempts"], 1)

            self.assertIsNotNone(total["three_point_shot_statistics"])
            self.assertEqual(total["three_point_shot_statistics"].keys(),
                             {"field_goal_percentage", "assisted_percentage", "percentage_of_total_field_goal_attempts",
                              "corner", "beyond_half_court"})

            self.assertGreaterEqual(total["three_point_shot_statistics"]["field_goal_percentage"], 0)
            self.assertLessEqual(total["three_point_shot_statistics"]["field_goal_percentage"], 1)
            self.assertGreaterEqual(total["three_point_shot_statistics"]["assisted_percentage"], 0)
            self.assertLessEqual(total["three_point_shot_statistics"]["assisted_percentage"], 1)
            self.assertGreaterEqual(total["three_point_shot_statistics"]["percentage_of_total_field_goal_attempts"], 0)
            self.assertLessEqual(total["three_point_shot_statistics"]["percentage_of_total_field_goal_attempts"], 1)

            self.assertIsNotNone(total["three_point_shot_statistics"]["corner"])
            self.assertEqual(total["three_point_shot_statistics"]["corner"].keys(),
                             {"field_goal_percentage", "percentage_of_three_point_field_goal_attempts"})
            self.assertGreaterEqual(total["three_point_shot_statistics"]["field_goal_percentage"], 0)
            self.assertLessEqual(total["three_point_shot_statistics"]["field_goal_percentage"], 1)
            self.assertGreaterEqual(total["three_point_shot_statistics"]["percentage_of_total_field_goal_attempts"], 0)
            self.assertLessEqual(total["three_point_shot_statistics"]["percentage_of_total_field_goal_attempts"], 1)

            self.assertIsNotNone(total["three_point_shot_statistics"]["beyond_half_court"])
            self.assertEqual(total["three_point_shot_statistics"]["beyond_half_court"].keys(), {"attempts", "made"})
            self.assertGreaterEqual(total["three_point_shot_statistics"]["beyond_half_court"]["attempts"], 0)
            self.assertGreaterEqual(total["three_point_shot_statistics"]["beyond_half_court"]["made"], 0)

class TestRoster(BaseEndToEndTest):
    def test_2026_celtics(self):
        boston_2026_roster = roster(team=Team.BOSTON_CELTICS, season_end_year=2026)
        for teammate in boston_2026_roster:
            self.assertIsNotNone(teammate)
            self.assertTrue(teammate["name"])
            self.assertTrue(teammate["slug"])
            self.assertTrue(teammate["number"])
            self.assertTrue(teammate["position"])

class TestContracts(BaseEndToEndTest):
    def test_contracts(self):
        contracts = []
        player_contracts(player_contract_processor=lambda contract: contracts.append(contract))
        self.assertGreaterEqual(len(contracts), 1)

        for contract in contracts:
            self.assertIsNotNone(contract)
            self.assertIsNotNone(contract.player)
            self.assertIsNotNone(contract.player.identifier)
            self.assertGreaterEqual(len(contract.player.identifier), 1)

            self.assertIsNotNone(contract.player.name)
            self.assertGreaterEqual(len(contract.player.name), 1)

            self.assertIsNotNone(contract.team)

            self.assertIsNotNone(contract.salaries_by_season_start_year)
            self.assertGreaterEqual(len(contract.salaries_by_season_start_year.keys()), 1)
