from unittest import TestCase

import requests
from lxml import html

from basketball_reference_web_scraper.data import Team, Position, TEAM_ABBREVIATIONS_TO_TEAM, \
    POSITION_ABBREVIATIONS_TO_POSITION
from basketball_reference_web_scraper.html import PlayerAdvancedSeasonTotalsTable
from basketball_reference_web_scraper.parsers import PlayerAdvancedSeasonTotalsParser, PositionAbbreviationParser, \
    TeamAbbreviationParser


class TestPlayersAdvancedSeasonTotals(TestCase):
    def setUp(self):
        self.season_2019_totals = requests.get(
            'https://www.basketball-reference.com/leagues/NBA_2019_advanced.html'
        ).text
        self.parser = PlayerAdvancedSeasonTotalsParser(
            position_abbreviation_parser=PositionAbbreviationParser(
                abbreviations_to_positions=POSITION_ABBREVIATIONS_TO_POSITION
            ),
            team_abbreviation_parser=TeamAbbreviationParser(
                abbreviations_to_teams=TEAM_ABBREVIATIONS_TO_TEAM,
            ),
        )
        self.season_2019_totals_table = PlayerAdvancedSeasonTotalsTable(html=html.fromstring(self.season_2019_totals))

    def test_2019_jimmy_butler_philly_season_totals(self):
        parsed_season_totals = self.parser.parse(totals=self.season_2019_totals_table.get_rows())

        philly_jimmy_butler = parsed_season_totals[94]

        self.assertEqual(philly_jimmy_butler["slug"], "butleji01")
        self.assertEqual(philly_jimmy_butler["name"], "Jimmy Butler")
        self.assertEqual(philly_jimmy_butler["positions"], [Position.SMALL_FORWARD])
        self.assertEqual(philly_jimmy_butler["team"], Team.PHILADELPHIA_76ERS)
        self.assertEqual(philly_jimmy_butler["games_played"], 55)
        self.assertEqual(philly_jimmy_butler["minutes_played"], 1824)
        self.assertEqual(philly_jimmy_butler["player_efficiency_rating"], 19.8)
        self.assertEqual(philly_jimmy_butler["true_shooting_percentage"], 0.569)
        self.assertEqual(philly_jimmy_butler["three_point_attempt_rate"], 0.198)
        self.assertEqual(philly_jimmy_butler["free_throw_attempt_rate"], 0.407)
        self.assertEqual(philly_jimmy_butler["offensive_rebound_percentage"], 6.3)
        self.assertEqual(philly_jimmy_butler["defensive_rebound_percentage"], 10.4)
        self.assertEqual(philly_jimmy_butler["total_rebound_percentage"], 8.4)
        self.assertEqual(philly_jimmy_butler["assist_percentage"], 18.0)
        self.assertEqual(philly_jimmy_butler["steal_percentage"], 2.6)
        self.assertEqual(philly_jimmy_butler["block_percentage"], 1.2)
        self.assertEqual(philly_jimmy_butler["turnover_percentage"], 8.4)
        self.assertEqual(philly_jimmy_butler["usage_percentage"], 22.1)
        self.assertEqual(philly_jimmy_butler["offensive_win_shares"], 4.4)
        self.assertEqual(philly_jimmy_butler["defensive_win_shares"], 2.1)
        self.assertEqual(philly_jimmy_butler["win_shares"], 6.6)
        self.assertEqual(philly_jimmy_butler["win_shares_per_48_minutes"], 0.172)
        self.assertEqual(philly_jimmy_butler["offensive_box_plus_minus"], 2.4)
        self.assertEqual(philly_jimmy_butler["defensive_box_plus_minus"], 0.7)
        self.assertEqual(philly_jimmy_butler["box_plus_minus"], 3.1)
        self.assertEqual(philly_jimmy_butler["value_over_replacement_player"], 2.4)

    def test_2019_jimmy_butler_combined_season_totals(self):
        parsed_season_totals = self.parser.parse(totals=self.season_2019_totals_table.get_rows(include_combined_totals=True))

        philly_jimmy_butler = parsed_season_totals[102]

        self.assertEqual(philly_jimmy_butler["slug"], "butleji01")
        self.assertEqual(philly_jimmy_butler["name"], "Jimmy Butler")
        self.assertEqual(philly_jimmy_butler["positions"], [Position.SMALL_FORWARD, Position.SHOOTING_GUARD])
        self.assertEqual(philly_jimmy_butler["team"], None)
        self.assertEqual(philly_jimmy_butler["games_played"], 65)
        self.assertEqual(philly_jimmy_butler["minutes_played"], 2185)
        self.assertEqual(philly_jimmy_butler["player_efficiency_rating"], 20.2)
        self.assertEqual(philly_jimmy_butler["true_shooting_percentage"], 0.571)
        self.assertEqual(philly_jimmy_butler["three_point_attempt_rate"], 0.213)
        self.assertEqual(philly_jimmy_butler["free_throw_attempt_rate"], 0.404)
        self.assertEqual(philly_jimmy_butler["offensive_rebound_percentage"], 6.0)
        self.assertEqual(philly_jimmy_butler["defensive_rebound_percentage"], 10.5)
        self.assertEqual(philly_jimmy_butler["total_rebound_percentage"], 8.3)
        self.assertEqual(philly_jimmy_butler["assist_percentage"], 18.0)
        self.assertEqual(philly_jimmy_butler["steal_percentage"], 2.7)
        self.assertEqual(philly_jimmy_butler["block_percentage"], 1.4)
        self.assertEqual(philly_jimmy_butler["turnover_percentage"], 8.2)
        self.assertEqual(philly_jimmy_butler["usage_percentage"], 22.3)
        self.assertEqual(philly_jimmy_butler["offensive_win_shares"], 5.4)
        self.assertEqual(philly_jimmy_butler["defensive_win_shares"], 2.5)
        self.assertEqual(philly_jimmy_butler["win_shares"], 7.9)
        self.assertEqual(philly_jimmy_butler["win_shares_per_48_minutes"], 0.173)
        self.assertEqual(philly_jimmy_butler["offensive_box_plus_minus"], 2.8)
        self.assertEqual(philly_jimmy_butler["defensive_box_plus_minus"], 0.9)
        self.assertEqual(philly_jimmy_butler["box_plus_minus"], 3.7)
        self.assertEqual(philly_jimmy_butler["value_over_replacement_player"], 3.2)
