from unittest import TestCase

from basketball_reference_web_scraper.data import Outcome, Location, Team
from basketball_reference_web_scraper.parsers import box_scores


class TestBoxScores(TestCase):
    def setUp(self):
        with open('./12_18_2015_daily_leaders.html', 'r') as december_18_2015_daily_leaders_html:
            self.december_18_2015_daily_leaders = december_18_2015_daily_leaders_html.read()

        with open('./01_29_2017_daily_leaders.html', 'r') as january_01_2017_daily_leaders_html:
            self.january_01_2017_daily_leaders = january_01_2017_daily_leaders_html.read()

    def test_box_scores_for_12_18_2015(self):
        parsed_box_score = box_scores.parse_box_score(self.december_18_2015_daily_leaders)
        self.assertEqual(len(parsed_box_score), 250)

    # Test for minutes played greater than or equal to 60 minutes
    def test_box_scores_for_01_01_2017(self):
        parsed_box_score = box_scores.parse_box_score(self.january_01_2017_daily_leaders)
        self.assertEqual(len(parsed_box_score), 170)

        first_box_score = parsed_box_score[0]

        self.assertEqual(first_box_score["name"], "Paul Millsap")
        self.assertEqual(first_box_score["team"], Team.ATLANTA_HAWKS)
        self.assertEqual(first_box_score["opponent"], Team.NEW_YORK_KNICKS)
        self.assertEqual(first_box_score["outcome"], Outcome.WIN)
        self.assertEqual(first_box_score["seconds_played"], 3607)
        self.assertEqual(first_box_score["made_field_goals"], 13)
        self.assertEqual(first_box_score["attempted_field_goals"], 29)
        self.assertEqual(first_box_score["made_three_point_field_goals"], 3)
        self.assertEqual(first_box_score["attempted_three_point_field_goals"], 8)
        self.assertEqual(first_box_score["made_free_throws"], 8)
        self.assertEqual(first_box_score["attempted_free_throws"], 10)
        self.assertEqual(first_box_score["offensive_rebounds"], 8)
        self.assertEqual(first_box_score["defensive_rebounds"], 11)
        self.assertEqual(first_box_score["assists"], 7)
        self.assertEqual(first_box_score["steals"], 1)
        self.assertEqual(first_box_score["blocks"], 0)
        self.assertEqual(first_box_score["turnovers"], 3)
        self.assertEqual(first_box_score["personal_fouls"], 4)
        self.assertEqual(first_box_score["game_score"], 31.3)
