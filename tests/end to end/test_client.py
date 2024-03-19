from unittest import TestCase

from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Location, Team, Outcome


class TestPlayerBoxScores(TestCase):
    def test(self):
        box_scores = client.player_box_scores(day=11, month=3, year=2024)
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
