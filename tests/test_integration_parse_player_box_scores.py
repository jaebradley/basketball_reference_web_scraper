import os
from unittest import TestCase

from basketball_reference_web_scraper.data import Team, Outcome
from basketball_reference_web_scraper.parsers.box_scores import players

november_03_2003_daily_leaders_html = os.path.join(os.path.dirname(__file__), './11_03_2003_daily_leaders.html')
november_01_2006_daily_leaders_html = os.path.join(os.path.dirname(__file__), './11_01_2006_daily_leaders.html')
december_18_2015_daily_leaders_html = os.path.join(os.path.dirname(__file__), './12_18_2015_daily_leaders.html')
december_12_2017_daily_leaders_html = os.path.join(os.path.dirname(__file__), './12_12_2017_daily_leaders.html')
january_01_2017_daily_leaders_html = os.path.join(os.path.dirname(__file__), './01_29_2017_daily_leaders.html')


class TestPlayerBoxScores(TestCase):
    def setUp(self):
        self.november_01_2006_daily_leaders = open(november_01_2006_daily_leaders_html).read()
        self.december_18_2015_daily_leaders = open(december_18_2015_daily_leaders_html).read()
        self.november_03_2003_daily_leaders = open(november_03_2003_daily_leaders_html).read()
        self.december_12_2017_daily_leaders = open(december_12_2017_daily_leaders_html).read()
        self.january_01_2017_daily_leaders = open(january_01_2017_daily_leaders_html).read()

    def test_box_scores_for_12_18_2015(self):
        parsed_box_score = players.parse_player_box_scores(self.december_18_2015_daily_leaders)
        self.assertEqual(len(parsed_box_score), 250)

    def test_box_scores_for_12_12_2017(self):
        parsed_box_score = players.parse_player_box_scores(self.december_12_2017_daily_leaders)
        self.assertEqual(len(parsed_box_score), 149)

    def test_parses_blank_value_for_andrew_bogut_on_12_12_2017(self):
        parsed_box_score = players.parse_player_box_scores(self.december_12_2017_daily_leaders)
        andrew_bogut = parsed_box_score[128]
        self.assertEqual(andrew_bogut["made_three_point_field_goals"], 0)
        self.assertEqual(andrew_bogut["attempted_three_point_field_goals"], 0)

    # Test for minutes played greater than or equal to 60 minutes
    def test_box_scores_for_01_01_2017(self):
        parsed_box_score = players.parse_player_box_scores(self.january_01_2017_daily_leaders)
        self.assertEqual(len(parsed_box_score), 170)

        first_box_score = parsed_box_score[0]

        self.assertEqual(first_box_score["slug"], "millspa01")
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

    def test_parses_new_orleans_hornets_for_box_scores_for_11_03_2003(self):
        parsed_box_score = players.parse_player_box_scores(self.november_03_2003_daily_leaders)

        self.assertEqual(len(parsed_box_score), 145)

        pj_brown = parsed_box_score[51]

        self.assertEqual(pj_brown["slug"], "brownpj01")
        self.assertEqual(pj_brown["name"], "P.J. Brown")
        self.assertEqual(pj_brown["team"], Team.NEW_ORLEANS_HORNETS)

    def test_parses_new_orleans_oklahoma_city_hornets_for_box_scores_for_11_01_2006(self):
        parsed_box_score = players.parse_player_box_scores(self.november_01_2006_daily_leaders)
        self.assertEqual(len(parsed_box_score), 272)

        chris_paul = parsed_box_score[10]

        self.assertEqual(chris_paul["slug"], "paulch01")
        self.assertEqual(chris_paul["name"], "Chris Paul")
        self.assertEqual(chris_paul["team"], Team.NEW_ORLEANS_OKLAHOMA_CITY_HORNETS)