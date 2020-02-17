from unittest import TestCase
from unittest.mock import MagicMock

from basketball_reference_web_scraper.parsers import TeamTotalsParser, TeamAbbreviationParser
from basketball_reference_web_scraper.data import Outcome, TeamTotal, TEAM_ABBREVIATIONS_TO_TEAM


class TestTeamTotalsParser(TestCase):
    def setUp(self):
        self.parser = TeamTotalsParser(
            team_abbreviation_parser=TeamAbbreviationParser(
                abbreviations_to_teams=TEAM_ABBREVIATIONS_TO_TEAM
            )
        )

    def test_parse_none_outcome_when_points_are_same(self):
        team_totals = TeamTotal(team_abbreviation="BOS", totals=MagicMock(points="100"))
        opposing_team_totals = TeamTotal(team_abbreviation="GSW", totals=MagicMock(points="100"))
        self.assertIsNone(
            self.parser.parse_totals(team_totals=team_totals, opposing_team_totals=opposing_team_totals)["outcome"]
        )
