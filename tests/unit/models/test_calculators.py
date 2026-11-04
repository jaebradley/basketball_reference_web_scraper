import datetime
import unittest

from basketball_reference_web_scraper.data import TeamAbbreviation, Team
from basketball_reference_web_scraper.models.calculators import (
    calculate_team_abbreviation,
    calculate_team_abbreviation_from_team_and_season,
)


class TestCalculatingTeamAbbreviations(unittest.TestCase):
    def test_charlotte_hornets_on_may_15_2002(self):
        self.assertEqual(
            calculate_team_abbreviation(
                team=Team.CHARLOTTE_HORNETS,
                date=datetime.date(year=2002, month=5, day=15),
            ),
            TeamAbbreviation.CHH,
        )

    def test_charlotte_hornets_on_may_16_2002(self):
        self.assertEqual(
            calculate_team_abbreviation(
                team=Team.CHARLOTTE_HORNETS,
                date=datetime.date(year=2002, month=5, day=16),
            ),
            TeamAbbreviation.CHO,
        )

    def test_invalid_team_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "CHUCK NORRIS is not a valid Team"):
            calculate_team_abbreviation(
                team="CHUCK NORRIS", date=datetime.date(year=2018, month=1, day=1)
            )

    def test_invalid_team_raises_value_error_for_season_calculation(self):
        with self.assertRaisesRegex(ValueError, "CHUCK NORRIS is not a valid Team"):
            calculate_team_abbreviation_from_team_and_season(
                team="CHUCK NORRIS", season_end_year=2018
            )
