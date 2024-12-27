import os
from unittest import TestCase

from lxml import html

from basketball_reference_web_scraper.data import Team, Position, POSITION_ABBREVIATIONS_TO_POSITION, \
    TEAM_ABBREVIATIONS_TO_TEAM
from basketball_reference_web_scraper.html import PlayerSeasonTotalTable
from basketball_reference_web_scraper.parsers import PositionAbbreviationParser, TeamAbbreviationParser, \
    PlayerSeasonTotalsParser


class BasePlayerSeasonTotalsTestCase(TestCase):
    _season_end_year = None

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(
                os.path.dirname(__file__),
                f"../files/players_season_totals/{cls._season_end_year}.html",
        ), 'r') as file_input: _html = file_input.read()
        cls._parsed_season_totals = PlayerSeasonTotalsParser(
            position_abbreviation_parser=PositionAbbreviationParser(
                abbreviations_to_positions=POSITION_ABBREVIATIONS_TO_POSITION
            ),
            team_abbreviation_parser=TeamAbbreviationParser(
                abbreviations_to_teams=TEAM_ABBREVIATIONS_TO_TEAM,
            )
        ).parse(PlayerSeasonTotalTable(html=html.fromstring(_html)).rows)


class Test2001PlayerSeasonTotals(BasePlayerSeasonTotalsTestCase):
    _season_end_year = 2001

    def test_length(self):
        self.assertEqual(len(Test2001PlayerSeasonTotals._parsed_season_totals), 490)

    def test_mahmoud_abdul_rauf(self):
        mahmoud_abdul_rauf = Test2001PlayerSeasonTotals._parsed_season_totals[279]

        self.assertEqual(mahmoud_abdul_rauf["slug"], "abdulma02")
        self.assertEqual(mahmoud_abdul_rauf["name"], "Mahmoud Abdul-Rauf")
        self.assertEqual(mahmoud_abdul_rauf["positions"], [Position.POINT_GUARD])
        self.assertEqual(mahmoud_abdul_rauf["team"], Team.VANCOUVER_GRIZZLIES)
        self.assertEqual(mahmoud_abdul_rauf["games_played"], 41)
        self.assertEqual(mahmoud_abdul_rauf["games_started"], 0)
        self.assertEqual(mahmoud_abdul_rauf["minutes_played"], 486)
        self.assertEqual(mahmoud_abdul_rauf["made_field_goals"], 120)
        self.assertEqual(mahmoud_abdul_rauf["attempted_field_goals"], 246)
        self.assertEqual(mahmoud_abdul_rauf["made_three_point_field_goals"], 4)
        self.assertEqual(mahmoud_abdul_rauf["attempted_three_point_field_goals"], 14)
        self.assertEqual(mahmoud_abdul_rauf["made_free_throws"], 22)
        self.assertEqual(mahmoud_abdul_rauf["attempted_free_throws"], 29)
        self.assertEqual(mahmoud_abdul_rauf["offensive_rebounds"], 5)
        self.assertEqual(mahmoud_abdul_rauf["defensive_rebounds"], 20)
        self.assertEqual(mahmoud_abdul_rauf["assists"], 76)
        self.assertEqual(mahmoud_abdul_rauf["steals"], 9)
        self.assertEqual(mahmoud_abdul_rauf["blocks"], 1)
        self.assertEqual(mahmoud_abdul_rauf["turnovers"], 26)
        self.assertEqual(mahmoud_abdul_rauf["personal_fouls"], 50)


class Test2018PlayerSeasonTotals(BasePlayerSeasonTotalsTestCase):
    _season_end_year = 2018

    def test_length(self):
        self.assertEqual(len(Test2018PlayerSeasonTotals._parsed_season_totals), 605)

    def test_alex_abrines(self):
        alex_abrines = Test2018PlayerSeasonTotals._parsed_season_totals[300]

        self.assertEqual(alex_abrines["slug"], "abrinal01")
        self.assertEqual(alex_abrines["name"], "Álex Abrines")
        self.assertEqual(alex_abrines["positions"], [Position.SHOOTING_GUARD])
        self.assertEqual(alex_abrines["team"], Team.OKLAHOMA_CITY_THUNDER)
        self.assertEqual(alex_abrines["games_played"], 75)
        self.assertEqual(alex_abrines["games_started"], 8)
        self.assertEqual(alex_abrines["minutes_played"], 1134)
        self.assertEqual(alex_abrines["made_field_goals"], 115)
        self.assertEqual(alex_abrines["attempted_field_goals"], 291)
        self.assertEqual(alex_abrines["made_three_point_field_goals"], 84)
        self.assertEqual(alex_abrines["attempted_three_point_field_goals"], 221)
        self.assertEqual(alex_abrines["made_free_throws"], 39)
        self.assertEqual(alex_abrines["attempted_free_throws"], 46)
        self.assertEqual(alex_abrines["offensive_rebounds"], 26)
        self.assertEqual(alex_abrines["defensive_rebounds"], 88)
        self.assertEqual(alex_abrines["assists"], 28)
        self.assertEqual(alex_abrines["steals"], 38)
        self.assertEqual(alex_abrines["blocks"], 8)
        self.assertEqual(alex_abrines["turnovers"], 25)
        self.assertEqual(alex_abrines["personal_fouls"], 124)

    def test_omer_asik(self):
        pelicans_omer_asik = Test2018PlayerSeasonTotals._parsed_season_totals[528]

        self.assertEqual(pelicans_omer_asik["slug"], "asikom01")
        self.assertEqual(pelicans_omer_asik["name"], "Ömer Aşık")
        self.assertEqual(pelicans_omer_asik["positions"], [Position.CENTER])
        self.assertEqual(pelicans_omer_asik["team"], Team.NEW_ORLEANS_PELICANS)
        self.assertEqual(pelicans_omer_asik["games_played"], 14)
        self.assertEqual(pelicans_omer_asik["games_started"], 0)
        self.assertEqual(pelicans_omer_asik["minutes_played"], 121)
        self.assertEqual(pelicans_omer_asik["made_field_goals"], 7)
        self.assertEqual(pelicans_omer_asik["attempted_field_goals"], 16)
        self.assertEqual(pelicans_omer_asik["made_three_point_field_goals"], 0)
        self.assertEqual(pelicans_omer_asik["attempted_three_point_field_goals"], 0)
        self.assertEqual(pelicans_omer_asik["made_free_throws"], 4)
        self.assertEqual(pelicans_omer_asik["attempted_free_throws"], 12)
        self.assertEqual(pelicans_omer_asik["offensive_rebounds"], 7)
        self.assertEqual(pelicans_omer_asik["defensive_rebounds"], 30)
        self.assertEqual(pelicans_omer_asik["assists"], 2)
        self.assertEqual(pelicans_omer_asik["steals"], 1)
        self.assertEqual(pelicans_omer_asik["blocks"], 2)
        self.assertEqual(pelicans_omer_asik["turnovers"], 5)
        self.assertEqual(pelicans_omer_asik["personal_fouls"], 14)

        bulls_omer_asik = Test2018PlayerSeasonTotals._parsed_season_totals[529]

        self.assertEqual(pelicans_omer_asik["slug"], "asikom01")
        self.assertEqual(bulls_omer_asik["name"], "Ömer Aşık")
        self.assertEqual(bulls_omer_asik["positions"], [Position.CENTER])
        self.assertEqual(bulls_omer_asik["team"], Team.CHICAGO_BULLS)
        self.assertEqual(bulls_omer_asik["games_played"], 4)
        self.assertEqual(bulls_omer_asik["games_started"], 0)
        self.assertEqual(bulls_omer_asik["minutes_played"], 61)
        self.assertEqual(bulls_omer_asik["made_field_goals"], 2)
        self.assertEqual(bulls_omer_asik["attempted_field_goals"], 6)
        self.assertEqual(bulls_omer_asik["made_three_point_field_goals"], 0)
        self.assertEqual(bulls_omer_asik["attempted_three_point_field_goals"], 0)
        self.assertEqual(bulls_omer_asik["made_free_throws"], 0)
        self.assertEqual(bulls_omer_asik["attempted_free_throws"], 1)
        self.assertEqual(bulls_omer_asik["offensive_rebounds"], 2)
        self.assertEqual(bulls_omer_asik["defensive_rebounds"], 8)
        self.assertEqual(bulls_omer_asik["assists"], 1)
        self.assertEqual(bulls_omer_asik["steals"], 1)
        self.assertEqual(bulls_omer_asik["blocks"], 2)
        self.assertEqual(bulls_omer_asik["turnovers"], 4)
        self.assertEqual(bulls_omer_asik["personal_fouls"], 6)


class Test2019PlayerSeasonTotals(BasePlayerSeasonTotalsTestCase):
    _season_end_year = 2019

    def test_jimmy_butler(self):
        philly_jimmy_butler = Test2019PlayerSeasonTotals._parsed_season_totals[60]

        self.assertEqual(philly_jimmy_butler["slug"], "butleji01")
        self.assertEqual(philly_jimmy_butler["name"], "Jimmy Butler")
        self.assertEqual(philly_jimmy_butler["positions"], [Position.SMALL_FORWARD])
        self.assertEqual(philly_jimmy_butler["team"], Team.PHILADELPHIA_76ERS)
        self.assertEqual(philly_jimmy_butler["games_played"], 55)
        self.assertEqual(philly_jimmy_butler["games_started"], 55)
        self.assertEqual(philly_jimmy_butler["minutes_played"], 1824)
        self.assertEqual(philly_jimmy_butler["made_field_goals"], 344)
        self.assertEqual(philly_jimmy_butler["attempted_field_goals"], 747)
        self.assertEqual(philly_jimmy_butler["made_three_point_field_goals"], 50)
        self.assertEqual(philly_jimmy_butler["attempted_three_point_field_goals"], 148)
        self.assertEqual(philly_jimmy_butler["made_free_throws"], 264)
        self.assertEqual(philly_jimmy_butler["attempted_free_throws"], 304)
        self.assertEqual(philly_jimmy_butler["offensive_rebounds"], 105)
        self.assertEqual(philly_jimmy_butler["defensive_rebounds"], 185)
        self.assertEqual(philly_jimmy_butler["assists"], 220)
        self.assertEqual(philly_jimmy_butler["steals"], 99)
        self.assertEqual(philly_jimmy_butler["blocks"], 29)
        self.assertEqual(philly_jimmy_butler["turnovers"], 81)
        self.assertEqual(philly_jimmy_butler["personal_fouls"], 93)
