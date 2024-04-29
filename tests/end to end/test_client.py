import datetime
import os
import time
from unittest import TestCase

from basketball_reference_web_scraper.client import player_box_scores, season_schedule, players_advanced_season_totals, \
    play_by_play
from basketball_reference_web_scraper.data import Location, Outcome
from basketball_reference_web_scraper.data import OutputWriteOption, OutputType, Team, PeriodType


class TestClient(TestCase):
    def setUp(self):
        # To avoid getting rate-limited
        time.sleep(20)

    def test_player_box_scores(self):
        box_scores = player_box_scores(day=11, month=3, year=2024)
        self.assertIsNotNone(box_scores)
        self.assertNotEqual(0, len(box_scores))
        self.assertEqual(124, len(box_scores))
        self.assertEqual({
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
            "game_score": 42.5,
        },
            box_scores[0])

    def test_2001_season_schedule(self):
        schedule = season_schedule(season_end_year=2001)
        self.assertIsNotNone(schedule)

    def test_current_year_season_schedule(self):
        season_schedule = season_schedule(season_end_year=datetime.datetime.now().year)
        self.assertIsNotNone(season_schedule)

    def test_2019_player_advanced_season_totals(self):
        player_season_totals = players_advanced_season_totals(season_end_year=2019)
        self.assertIsNotNone(player_season_totals)
        self.assertTrue(len(player_season_totals) > 0)

    def test_BOS_2018_10_16_play_by_play(self):
        play_by_play = play_by_play(
            home_team=Team.BOSTON_CELTICS,
            day=16,
            month=10,
            year=2018,
        )
        self.assertIsNotNone(play_by_play)

    def test_BOS_2018_10_16_play_by_play_csv_to_file(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/2018_10_16_BOS_pbp.csv",
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

    def test_overtime_play_by_play(self):
        play_by_play = play_by_play(
            home_team=Team.PORTLAND_TRAIL_BLAZERS,
            day=22,
            month=10,
            year=2018,
        )
        last_play = play_by_play[-1]
        self.assertIsNotNone(last_play)
        self.assertEqual(1, last_play["period"])
        self.assertEqual(PeriodType.OVERTIME, last_play["period_type"])

    def test_overtime_play_by_play_to_json_file(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/2018_10_22_POR_pbp.json",
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
