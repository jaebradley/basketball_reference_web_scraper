from unittest import TestCase
from unittest.mock import MagicMock

from basketball_reference_web_scraper.data import TeamTotal
from basketball_reference_web_scraper.parsers import TeamTotalsParser, TeamAbbreviationParser


class TestTeamTotalsParser(TestCase):
    def setUp(self):
        self.parser = TeamTotalsParser(
            team_abbreviation_parser=TeamAbbreviationParser()
        )

    def test_parse_none_outcome_when_points_are_same(self):
        team_totals = TeamTotal(
            basic_statistics_table=MagicMock(team_totals=MagicMock(points="100"), team_abbreviation="foo"),
            advanced_statistics_table=MagicMock(team_abbreviation="foo"))
        opposing_team_totals = TeamTotal(
            basic_statistics_table=MagicMock(team_totals=MagicMock(points="100"), team_abbreviation="bar"),
            advanced_statistics_table=MagicMock(team_abbreviation="bar"))
        self.assertIsNone(
            self.parser.parse_totals(team_totals=team_totals, opposing_team_totals=opposing_team_totals)["outcome"]
        )
