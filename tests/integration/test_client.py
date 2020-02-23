from datetime import datetime
from unittest import TestCase
import os

import basketball_reference_web_scraper.client as client
from basketball_reference_web_scraper.data import OutputWriteOption, OutputType, Team, PeriodType


class TestClient(TestCase):
    def test_schedules_from_2001(self):
        now = datetime.now()
        current_year = now.year

        for year in range(2001, current_year + 1):
            season_schedule = client.season_schedule(season_end_year=year)
            self.assertIsNotNone(season_schedule)

    def test_output_json_box_scores_to_file(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/foo.json",
        )
        client.player_box_scores(
            day=1,
            month=1,
            year=2001,
            output_type=OutputType.JSON,
            output_file_path=output_file_path,
            output_write_option=OutputWriteOption.WRITE
        )

    def test_output_csv_box_scores_to_file(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/2003_10_29_TOR_pbp.csv",
        )
        client.player_box_scores(
            day=1,
            month=1,
            year=2001,
            output_type=OutputType.CSV,
            output_file_path=output_file_path,
            output_write_option=OutputWriteOption.WRITE
        )

    def test_output_json_box_scores_to_memory(self):
        january_first_box_scores = client.player_box_scores(
            day=1,
            month=1,
            year=2001,
            output_type=OutputType.JSON,
        )

        self.assertIsNotNone(january_first_box_scores)

    def test_2001_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2001)
        self.assertIsNotNone(schedule)

    def test_2002_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2002)
        self.assertIsNotNone(schedule)

    def test_2003_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2003)
        self.assertIsNotNone(schedule)

    def test_2004_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2004)
        self.assertIsNotNone(schedule)

    def test_2005_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2005)
        self.assertIsNotNone(schedule)

    def test_2006_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2006)
        self.assertIsNotNone(schedule)

    def test_2007_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2007)
        self.assertIsNotNone(schedule)

    def test_2008_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2008)
        self.assertIsNotNone(schedule)

    def test_2009_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2009)
        self.assertIsNotNone(schedule)

    def test_2010_season_schedule(self):
        player_season_totals = client.season_schedule(season_end_year=2010)
        self.assertIsNotNone(player_season_totals)

    def test_2011_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2011)
        self.assertIsNotNone(schedule)

    def test_2012_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2012)
        self.assertIsNotNone(schedule)

    def test_2013_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2013)
        self.assertIsNotNone(schedule)

    def test_2014_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2014)
        self.assertIsNotNone(schedule)

    def test_2015_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2015)
        self.assertIsNotNone(schedule)

    def test_2016_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2016)
        self.assertIsNotNone(schedule)

    def test_2017_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2017)
        self.assertIsNotNone(schedule)

    def test_2018_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2018)
        self.assertIsNotNone(schedule)

    def test_2019_season_schedule(self):
        schedule = client.season_schedule(season_end_year=2019)
        self.assertIsNotNone(schedule)

    def test_2019_player_advanced_season_totals(self):
        player_season_totals = client.players_advanced_season_totals(season_end_year=2019)
        self.assertIsNotNone(player_season_totals)
        self.assertTrue(len(player_season_totals) > 0)

    def test_BOS_2018_10_16_play_by_play(self):
        play_by_play = client.play_by_play(
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
        client.play_by_play(
            home_team=Team.BOSTON_CELTICS,
            day=16,
            month=10,
            year=2018,
            output_type=OutputType.CSV,
            output_file_path=output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )

    def test_overtime_play_by_play(self):
        play_by_play = client.play_by_play(
            home_team=Team.PORTLAND_TRAIL_BLAZERS,
            day=22,
            month=10,
            year=2018,
        )
        last_play = play_by_play[-1]
        self.assertIsNotNone(last_play)
        self.assertEqual(1, last_play["period"])
        self.assertEqual(PeriodType.OVERTIME, last_play["period_type"])

    def test_overtime_play_by_play_to_csv(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/2018_10_22_POR_pbp.csv",
        )
        client.play_by_play(
            home_team=Team.PORTLAND_TRAIL_BLAZERS,
            day=22,
            month=10,
            year=2018,
            output_type=OutputType.CSV,
            output_file_path=output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )

    def test_BOS_2018_10_16_play_by_play_json_to_file(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/2018_10_16_BOS_pbp.json",
        )
        client.play_by_play(
            home_team=Team.BOSTON_CELTICS,
            day=16,
            month=10,
            year=2018,
            output_type=OutputType.JSON,
            output_file_path=output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )

    def test_overtime_play_by_play_to_json_file(self):
        output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/2018_10_22_POR_pbp.json",
        )
        client.play_by_play(
            home_team=Team.PORTLAND_TRAIL_BLAZERS,
            day=22,
            month=10,
            year=2018,
            output_type=OutputType.JSON,
            output_file_path=output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )
