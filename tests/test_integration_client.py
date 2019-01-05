from datetime import datetime
from unittest import TestCase

import basketball_reference_web_scraper.client as client
from basketball_reference_web_scraper.data import OutputWriteOption, OutputType


class TestClient(TestCase):
    def test_schedules_from_2001(self):
        now = datetime.now()
        current_year = now.year

        for year in range(2001, current_year + 1):
            season_schedule = client.season_schedule(season_end_year=year)
            self.assertIsNotNone(season_schedule)

    def test_output_json_box_scores_to_file(self):
        client.player_box_scores(
            day=1,
            month=1,
            year=2001,
            output_type=OutputType.JSON,
            output_file_path="./foo.json",
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

    # TODO: @jaebradley there's an open PR that's fixing this broken test
    # def test_2019_season_schedule(self):
    #     schedule = client.season_schedule(season_end_year=2019)
    #     self.assertIsNotNone(schedule)

    def test_2001_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2001)
        self.assertIsNotNone(player_season_totals)

    def test_2002_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2002)
        self.assertIsNotNone(player_season_totals)

    def test_2003_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2003)
        self.assertIsNotNone(player_season_totals)

    def test_2004_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2004)
        self.assertIsNotNone(player_season_totals)

    def test_2005_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2005)
        self.assertIsNotNone(player_season_totals)

    def test_2006_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2006)
        self.assertIsNotNone(player_season_totals)

    def test_2007_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2007)
        self.assertIsNotNone(player_season_totals)

    def test_2008_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2008)
        self.assertIsNotNone(player_season_totals)

    def test_2009_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2009)
        self.assertIsNotNone(player_season_totals)

    def test_2010_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2010)
        self.assertIsNotNone(player_season_totals)

    def test_2011_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2011)
        self.assertIsNotNone(player_season_totals)

    def test_2012_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2012)
        self.assertIsNotNone(player_season_totals)

    def test_2013_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2013)
        self.assertIsNotNone(player_season_totals)

    def test_2014_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2014)
        self.assertIsNotNone(player_season_totals)

    def test_2015_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2015)
        self.assertIsNotNone(player_season_totals)

    def test_2016_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2016)
        self.assertIsNotNone(player_season_totals)

    def test_2017_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2017)
        self.assertIsNotNone(player_season_totals)

    def test_2018_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2018)
        self.assertIsNotNone(player_season_totals)

    def test_2019_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2019)
        self.assertIsNotNone(player_season_totals)

    def test_2018_01_01_team_box_scores(self):
        team_box_scores = client.team_box_scores(day=1, month=1, year=2018)
        self.assertIsNotNone(team_box_scores)

    def test_2001_01_01_team_box_scores(self):
        team_box_scores = client.team_box_scores(day=1, month=1, year=2001)
        self.assertIsNotNone(team_box_scores)

    def test_2004_01_02_team_box_scores(self):
        team_box_scores = client.team_box_scores(day=2, month=1, year=2004)
        self.assertIsNotNone(team_box_scores)
