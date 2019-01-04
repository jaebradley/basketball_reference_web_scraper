from unittest import TestCase
import os

from basketball_reference_web_scraper.parsers.box_scores.teams import parse_team_totals
from basketball_reference_web_scraper.data import Team

atlanta_box_score_2017_01_01_html = os.path.join(os.path.dirname(__file__), './201701010ATL.html')


class TestParseTeams(TestCase):
    def setUp(self):
        self.atlanta_box_score_2017_01_01 = open(atlanta_box_score_2017_01_01_html).read()

    def test_parse_two_team_totals(self):
        team_totals = parse_team_totals(self.atlanta_box_score_2017_01_01)
        self.assertEqual(len(team_totals), 2)

    def test_parse_san_antonio_team_totals(self):
        team_totals = parse_team_totals(self.atlanta_box_score_2017_01_01)
        sas_team_totals = team_totals[0]
        self.assertEqual(sas_team_totals["team"], Team.SAN_ANTONIO_SPURS)
        self.assertEqual(sas_team_totals["minutes_played"], 265)
        self.assertEqual(sas_team_totals["made_field_goals"], 42)
        self.assertEqual(sas_team_totals["attempted_field_goals"], 90)
        self.assertEqual(sas_team_totals["made_three_point_field_goals"], 9)
        self.assertEqual(sas_team_totals["attempted_three_point_field_goals"], 27)
        self.assertEqual(sas_team_totals["made_free_throws"], 19)
        self.assertEqual(sas_team_totals["attempted_free_throws"], 22)
        self.assertEqual(sas_team_totals["offensive_rebounds"], 9)
        self.assertEqual(sas_team_totals["defensive_rebounds"], 38)
        self.assertEqual(sas_team_totals["assists"], 27)
        self.assertEqual(sas_team_totals["steals"], 5)
        self.assertEqual(sas_team_totals["blocks"], 6)
        self.assertEqual(sas_team_totals["turnovers"], 12)
        self.assertEqual(sas_team_totals["personal_fouls"], 21)

    def test_parse_atlanta_team_totals(self):
        team_totals = parse_team_totals(self.atlanta_box_score_2017_01_01)
        atl_team_totals = team_totals[1]
        self.assertEqual(atl_team_totals["team"], Team.ATLANTA_HAWKS)
        self.assertEqual(atl_team_totals["minutes_played"], 265)
        self.assertEqual(atl_team_totals["made_field_goals"], 42)
        self.assertEqual(atl_team_totals["attempted_field_goals"], 92)
        self.assertEqual(atl_team_totals["made_three_point_field_goals"], 14)
        self.assertEqual(atl_team_totals["attempted_three_point_field_goals"], 28)
        self.assertEqual(atl_team_totals["made_free_throws"], 16)
        self.assertEqual(atl_team_totals["attempted_free_throws"], 27)
        self.assertEqual(atl_team_totals["offensive_rebounds"], 11)
        self.assertEqual(atl_team_totals["defensive_rebounds"], 35)
        self.assertEqual(atl_team_totals["assists"], 25)
        self.assertEqual(atl_team_totals["steals"], 6)
        self.assertEqual(atl_team_totals["blocks"], 6)
        self.assertEqual(atl_team_totals["turnovers"], 11)
        self.assertEqual(atl_team_totals["personal_fouls"], 21)
