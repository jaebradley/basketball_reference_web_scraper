from unittest import TestCase

from basketball_reference_web_scraper.data import Team, TEAM_ABBREVIATIONS_BY_TEAM, TeamAbbreviation


class TestTeamAbbreviationsByTeam(TestCase):
    def test_each_team_has_an_abbreviation(self):
        self.assertEqual(set(set(TeamAbbreviation) - {TeamAbbreviation.CHH, TeamAbbreviation.BLB, TeamAbbreviation.DNN}),
                         set(map(lambda team: TEAM_ABBREVIATIONS_BY_TEAM.get(team), list(Team))))

    def test_charlotte_hornets(self):
        self.assertEqual(TeamAbbreviation.CHO, TEAM_ABBREVIATIONS_BY_TEAM.get(Team.CHARLOTTE_HORNETS))

    def test_denver_nuggets(self):
        self.assertEqual(TeamAbbreviation.DEN, TEAM_ABBREVIATIONS_BY_TEAM.get(Team.DENVER_NUGGETS))

    def test_baltimore_bullets(self):
        self.assertEqual(TeamAbbreviation.BAL, TEAM_ABBREVIATIONS_BY_TEAM.get(Team.BALTIMORE_BULLETS))
