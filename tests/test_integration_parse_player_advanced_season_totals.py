import os
from unittest import TestCase

from basketball_reference_web_scraper.data import Team, Position
from basketball_reference_web_scraper.parsers import players_advanced_season_totals

season_2019_totals_html = os.path.join(os.path.dirname(__file__), './NBA_2019_advanced_totals.html')


class TestPlayersSeasonTotals(TestCase):
    def setUp(self):

        self.season_2019_totals = open(season_2019_totals_html).read()

    def test_2019_jimmy_butler_season_totals(self):
        parsed_season_totals = players_advanced_season_totals.parse_players_advanced_season_totals(self.season_2019_totals)

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
        self.assertEqual(philly_jimmy_butler["defensive_box_plus_minus"], 0.5)
        self.assertEqual(philly_jimmy_butler["box_plus_minus"], 2.9)
        self.assertEqual(philly_jimmy_butler["value_over_replacement_player"], 2.3)
