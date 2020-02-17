from unittest import TestCase

from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Position, Team


class TestPlayerSeasonTotals(TestCase):
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

    def test_avery_bradley_2019_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2019)
        clippers_avery_bradley = player_season_totals[66]

        self.assertEqual('bradlav01', clippers_avery_bradley["slug"])
        self.assertEqual("Avery Bradley", clippers_avery_bradley["name"])
        self.assertListEqual([Position.SHOOTING_GUARD], clippers_avery_bradley["positions"])
        self.assertEqual(28, clippers_avery_bradley["age"])
        self.assertEqual(Team.LOS_ANGELES_CLIPPERS, clippers_avery_bradley["team"])
        self.assertEqual(49, clippers_avery_bradley["games_played"])
        self.assertEqual(49, clippers_avery_bradley["games_started"])
        self.assertEqual(1463, clippers_avery_bradley["minutes_played"])
        self.assertEqual(161, clippers_avery_bradley["made_field_goals"])
        self.assertEqual(420, clippers_avery_bradley["attempted_field_goals"])
        self.assertEqual(58, clippers_avery_bradley["made_three_point_field_goals"])
        self.assertEqual(172, clippers_avery_bradley["attempted_three_point_field_goals"])
        self.assertEqual(20, clippers_avery_bradley["made_free_throws"])
        self.assertEqual(25, clippers_avery_bradley["attempted_free_throws"])
        self.assertEqual(35, clippers_avery_bradley["offensive_rebounds"])
        self.assertEqual(96, clippers_avery_bradley["defensive_rebounds"])
        self.assertEqual(96, clippers_avery_bradley["assists"])
        self.assertEqual(27, clippers_avery_bradley["steals"])
        self.assertEqual(16, clippers_avery_bradley["blocks"])
        self.assertEqual(61, clippers_avery_bradley["turnovers"])
        self.assertEqual(133, clippers_avery_bradley["personal_fouls"])
        self.assertEqual(400, clippers_avery_bradley["points"])
