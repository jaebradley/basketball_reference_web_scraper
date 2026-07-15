import datetime
import unittest

from basketball_reference_web_scraper.data import TeamAbbreviation, Team
from basketball_reference_web_scraper.models.calculators import calculate_team_abbreviation


class TestCalculatingTeamAbbreviations(unittest.TestCase):
    def test_charlotte_hornets_on_may_15_2002(self):
        self.assertEqual(
            calculate_team_abbreviation(team=Team.CHARLOTTE_HORNETS, date=datetime.date(year=2002, month=5, day=15)),
            TeamAbbreviation.CHH
        )

    def test_charlotte_hornets_on_may_16_2002(self):
        self.assertEqual(
            calculate_team_abbreviation(team=Team.CHARLOTTE_HORNETS, date=datetime.date(year=2002, month=5, day=16)),
            TeamAbbreviation.CHO)
