import os
from unittest import TestCase

from lxml import html

from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM, TeamTotal
from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.html import BoxScoresPage
from basketball_reference_web_scraper.parsers import TeamAbbreviationParser, \
    TeamTotalsParser

atlanta_box_score_2017_01_01_html = os.path.join(os.path.dirname(__file__), './201701010ATL.html')


class TestParseTeams(TestCase):
    def setUp(self):
        self.atlanta_box_score_2017_01_01 = open(atlanta_box_score_2017_01_01_html).read()
        self.team_abbreviation_parser = TeamAbbreviationParser(
            abbreviations_to_teams=TEAM_ABBREVIATIONS_TO_TEAM,
        )
        self.page = BoxScoresPage(html.fromstring(self.atlanta_box_score_2017_01_01))
        self.combined_team_totals = [
            TeamTotal(team_abbreviation=table.team_abbreviation, totals=table.team_totals)
            for table in self.page.basic_statistics_tables
        ]
        self.parser = TeamTotalsParser(team_abbreviation_parser=self.team_abbreviation_parser)
        self.team_totals = self.parser.parse(self.combined_team_totals)

    def test_parse_two_team_totals(self):
        self.assertEqual(len(self.team_totals), 2)

    def test_parse_san_antonio_team_totals(self):
        sas_team_totals = self.team_totals[0]
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
        atl_team_totals = self.team_totals[1]
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
