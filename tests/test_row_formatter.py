from unittest import TestCase

from basketball_reference_web_scraper.data import Team, Location, Outcome, Position
from basketball_reference_web_scraper.writers import RowFormatter


class TestRowFormatter(TestCase):
    def test_away_team_data_field_name(self):
        formatter = RowFormatter(data_field_names=["away_team"])
        self.assertEqual(
            formatter.format(row_data={"away_team": Team.BOSTON_CELTICS}),
            {"away_team": Team.BOSTON_CELTICS.value}
        )

    def test_home_team_data_field_name(self):
        formatter = RowFormatter(data_field_names=["home_team"])
        self.assertEqual(
            formatter.format(row_data={"home_team": Team.BOSTON_CELTICS}),
            {"home_team": Team.BOSTON_CELTICS.value}
        )

    def test_team_data_field_name(self):
        formatter = RowFormatter(data_field_names=["team"])
        self.assertEqual(
            formatter.format(row_data={"team": Team.BOSTON_CELTICS}),
            {"team": Team.BOSTON_CELTICS.value}
        )

    def test_location_data_field_name(self):
        formatter = RowFormatter(data_field_names=["location"])
        self.assertEqual(
            formatter.format(row_data={"location": Location.HOME}),
            {"location": Location.HOME.value}
        )

    def test_opponent_data_field_name(self):
        formatter = RowFormatter(data_field_names=["opponent"])
        self.assertEqual(
            formatter.format(row_data={"opponent": Team.BOSTON_CELTICS}),
            {"opponent": Team.BOSTON_CELTICS.value}
        )

    def test_outcome_data_field_name(self):
        formatter = RowFormatter(data_field_names=["outcome"])
        self.assertEqual(
            formatter.format(row_data={"outcome": Outcome.WIN}),
            {"outcome": Outcome.WIN.value}
        )

    def test_empty_positions_data_field_name(self):
        formatter = RowFormatter(data_field_names=["positions"])
        self.assertEqual(
            formatter.format(row_data={"positions": []}),
            {"positions": ""}
        )

    def test_single_position_data_field_name(self):
        formatter = RowFormatter(data_field_names=["positions"])
        self.assertEqual(
            formatter.format(row_data={"positions": [Position.POINT_GUARD]}),
            {"positions": "POINT GUARD"}
        )

    def test_multiple_positions_data_field_name(self):
        formatter = RowFormatter(data_field_names=["positions"])
        self.assertEqual(
            formatter.format(row_data={"positions": [Position.POINT_GUARD, Position.SHOOTING_GUARD]}),
            {"positions": "POINT GUARD-SHOOTING GUARD"}
        )

    def test_non_team_outcome_location_position_data_field_name(self):
        formatter = RowFormatter(data_field_names=["name"])
        self.assertEqual(
            formatter.format(row_data={"name": "jaebaebae"}),
            {"name": "jaebaebae"}
        )
