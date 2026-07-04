import datetime
import os
from unittest import TestCase

from lxml import html

from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM, LOCATION_ABBREVIATIONS_TO_POSITION, \
    OUTCOME_ABBREVIATIONS_TO_OUTCOME
from basketball_reference_web_scraper.data import Team, Outcome
from basketball_reference_web_scraper.html import DailyLeadersPage
from basketball_reference_web_scraper.parsers import TeamAbbreviationParser, \
    LocationAbbreviationParser, OutcomeAbbreviationParser, \
    SecondsPlayedParser, PlayerBoxScoresParser


class BaseBoxScoresTestCase(TestCase):
    _date: datetime.date = None

    @classmethod
    def setUpClass(cls):
        year, month, day = cls._date.year, cls._date.month, cls._date.day
        with open(os.path.join(
                os.path.dirname(__file__),
                f"../files/player_box_scores/{year}/{month}/{day}.html",
        ), 'r') as file_input: _html = file_input.read()
        cls._parsed_results = PlayerBoxScoresParser(
            team_abbreviation_parser=TeamAbbreviationParser(
                abbreviations_to_teams=TEAM_ABBREVIATIONS_TO_TEAM
            ),
            location_abbreviation_parser=LocationAbbreviationParser(
                abbreviations_to_locations=LOCATION_ABBREVIATIONS_TO_POSITION
            ),
            outcome_abbreviation_parser=OutcomeAbbreviationParser(
                abbreviations_to_outcomes=OUTCOME_ABBREVIATIONS_TO_OUTCOME
            ),
            seconds_played_parser=SecondsPlayedParser(),
        ).parse(DailyLeadersPage(html=html.fromstring(_html)).daily_leaders)


class TestNovemberFirst2006(BaseBoxScoresTestCase):
    _date = datetime.date(year=2006, month=11, day=1)

    def test_length(self):
        self.assertEqual(len(self._parsed_results), 272)

    def test_new_orleans_oklahoma_city_hornets(self):
        chris_paul = self._parsed_results[10]

        self.assertEqual(chris_paul["slug"], "paulch01")
        self.assertEqual(chris_paul["name"], "Chris Paul")
        self.assertEqual(chris_paul["team"], Team.NEW_ORLEANS_OKLAHOMA_CITY_HORNETS)


class TestDecemberEighteenth2015(BaseBoxScoresTestCase):
    _date = datetime.date(year=2015, month=12, day=18)

    def test_length(self):
        self.assertEqual(len(self._parsed_results), 250)


class TestNovemberThird2003(BaseBoxScoresTestCase):
    _date = datetime.date(year=2003, month=11, day=3)

    def test_length(self):
        self.assertEqual(len(self._parsed_results), 145)

    def test_new_orleans_hornets(self):
        pj_brown = self._parsed_results[51]

        self.assertEqual(pj_brown["slug"], "brownpj01")
        self.assertEqual(pj_brown["name"], "P.J. Brown")
        self.assertEqual(pj_brown["team"], Team.NEW_ORLEANS_HORNETS)


class TestDecemberTwelfth2017(BaseBoxScoresTestCase):
    _date = datetime.date(year=2017, month=12, day=12)

    def test_length(self):
        self.assertEqual(len(self._parsed_results), 149)

    def test_andrew_bogut(self):
        andrew_bogut = self._parsed_results[128]
        self.assertEqual(andrew_bogut["made_three_point_field_goals"], 0)
        self.assertEqual(andrew_bogut["attempted_three_point_field_goals"], 0)


class TestJanuaryTwentyNinth2017(BaseBoxScoresTestCase):
    _date = datetime.date(year=2017, month=1, day=29)

    def test_length(self):
        self.assertEqual(len(self._parsed_results), 170)

    def test_paul_millsap(self):
        paul_millsap = self._parsed_results[0]

        self.assertEqual(paul_millsap["slug"], "millspa01")
        self.assertEqual(paul_millsap["name"], "Paul Millsap")
        self.assertEqual(paul_millsap["team"], Team.ATLANTA_HAWKS)
        self.assertEqual(paul_millsap["opponent"], Team.NEW_YORK_KNICKS)
        self.assertEqual(paul_millsap["outcome"], Outcome.WIN)
        self.assertEqual(paul_millsap["seconds_played"], 3607)
        self.assertEqual(paul_millsap["made_field_goals"], 13)
        self.assertEqual(paul_millsap["attempted_field_goals"], 29)
        self.assertEqual(paul_millsap["made_three_point_field_goals"], 3)
        self.assertEqual(paul_millsap["attempted_three_point_field_goals"], 8)
        self.assertEqual(paul_millsap["made_free_throws"], 8)
        self.assertEqual(paul_millsap["attempted_free_throws"], 10)
        self.assertEqual(paul_millsap["offensive_rebounds"], 8)
        self.assertEqual(paul_millsap["defensive_rebounds"], 11)
        self.assertEqual(paul_millsap["assists"], 7)
        self.assertEqual(paul_millsap["steals"], 1)
        self.assertEqual(paul_millsap["blocks"], 0)
        self.assertEqual(paul_millsap["turnovers"], 3)
        self.assertEqual(paul_millsap["personal_fouls"], 4)
        self.assertEqual(paul_millsap["game_score"], 31.3)
