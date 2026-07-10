import os
from unittest import TestCase

from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM, TeamTotal
from basketball_reference_web_scraper.data import Team, Outcome
from basketball_reference_web_scraper.html import BoxScoresPage
from basketball_reference_web_scraper.parsers import TeamAbbreviationParser, \
    TeamTotalsParser
from lxml import html


class TestParseTeams(TestCase):
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(
                os.path.dirname(__file__),
                f"../files/boxscores/2017/1/201701010ATL.html",
        ), 'r') as file_input: _html = file_input.read()
        tables = BoxScoresPage(html.fromstring(html=_html)).statistics_tables
        first_team_totals, second_team_totals = list(
            map(lambda paired_tables: TeamTotal(basic_statistics_table=paired_tables[0],
                                                advanced_statistics_table=paired_tables[1]),
                zip(tables[::2], tables[1::2])))
        cls._parsed_results = TeamTotalsParser(
            team_abbreviation_parser=TeamAbbreviationParser(
                abbreviations_to_teams=TEAM_ABBREVIATIONS_TO_TEAM
            ),
        ).parse(
            first_team_totals=first_team_totals,
            second_team_totals=second_team_totals,
        )

    def test_length(self):
        self.assertEqual(len(self._parsed_results), 2)

    def test_parse_san_antonio_team_totals(self):
        sas_team_totals = self._parsed_results[0]
        self.assertEqual(sas_team_totals["team"], Team.SAN_ANTONIO_SPURS)
        self.assertEqual(sas_team_totals["outcome"], Outcome.LOSS)
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
        self.assertEqual(sas_team_totals["points"], 112)
        self.assertEqual(sas_team_totals["true_shooting_percentage"], 0.562)
        self.assertEqual(sas_team_totals["effective_field_goal_percentage"], 0.517)
        self.assertEqual(sas_team_totals["three_point_attempt_rate"], 0.300)
        self.assertEqual(sas_team_totals["free_throw_attempt_rate"], 0.244)
        self.assertEqual(sas_team_totals["offensive_rebound_percentage"], 20.5)
        self.assertEqual(sas_team_totals["defensive_rebound_percentage"], 77.6)
        self.assertEqual(sas_team_totals["total_rebound_percentage"], 50.5)
        self.assertEqual(sas_team_totals["assist_percentage"], 64.3)
        self.assertEqual(sas_team_totals["steal_percentage"], 4.9)
        self.assertEqual(sas_team_totals["block_percentage"], 9.4)
        self.assertEqual(sas_team_totals["turnover_rate"], 10.7)
        self.assertEqual(sas_team_totals["offensive_rating"], 110.3)
        self.assertEqual(sas_team_totals["defensive_rating"], 112.3)

    def test_parse_atlanta_team_totals(self):
        atl_team_totals = self._parsed_results[1]
        self.assertEqual(atl_team_totals["team"], Team.ATLANTA_HAWKS)
        self.assertEqual(atl_team_totals["outcome"], Outcome.WIN)
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
        self.assertEqual(atl_team_totals["turnovers"], 12)
        self.assertEqual(atl_team_totals["personal_fouls"], 21)
        self.assertEqual(atl_team_totals["points"], 114)
        self.assertEqual(atl_team_totals["true_shooting_percentage"], 0.549)
        self.assertEqual(atl_team_totals["effective_field_goal_percentage"], 0.533)
        self.assertEqual(atl_team_totals["three_point_attempt_rate"], 0.304)
        self.assertEqual(atl_team_totals["free_throw_attempt_rate"], 0.293)
        self.assertEqual(atl_team_totals["offensive_rebound_percentage"], 22.4)
        self.assertEqual(atl_team_totals["defensive_rebound_percentage"], 79.5)
        self.assertEqual(atl_team_totals["total_rebound_percentage"], 49.5)
        self.assertEqual(atl_team_totals["assist_percentage"], 59.5)
        self.assertEqual(atl_team_totals["steal_percentage"], 5.9)
        self.assertEqual(atl_team_totals["block_percentage"], 9.5)
        self.assertEqual(atl_team_totals["turnover_rate"], 10.4)
        self.assertEqual(atl_team_totals["offensive_rating"], 112.3)
        self.assertEqual(atl_team_totals["defensive_rating"], 110.3)
