import filecmp
import os
from unittest import TestCase

import requests_mock

from basketball_reference_web_scraper.client import roster
from basketball_reference_web_scraper.data import Team, Position, OutputType, OutputWriteOption
from basketball_reference_web_scraper.errors import InvalidTeamSeason


class TestCSV2026RosterForBoston(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/teams/2026/BOS.html",
        ), 'r') as file_input: self._html = file_input.read();

        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "output/generated/rosters/BOS/2026.csv"
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "output/expected/rosters/BOS/2026.csv"
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    @requests_mock.Mocker()
    def test_output(self, m):
        m.get("https://www.basketball-reference.com/teams/BOS/2026.html", text=self._html, status_code=200)

        roster(
            team=Team.BOSTON_CELTICS,
            season_end_year=2026,
            output_type=OutputType.CSV,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )
        self.assertTrue(
            filecmp.cmp(
                self.output_file_path,
                self.expected_output_file_path))



class TestJSON2026RosterForBoston(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/teams/2026/BOS.html",
        ), 'r') as file_input: self._html = file_input.read();

        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "output/generated/rosters/BOS/2026.json"
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "output/expected/rosters/BOS/2026.json"
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    @requests_mock.Mocker()
    def test_output(self, m):
        m.get("https://www.basketball-reference.com/teams/BOS/2026.html", text=self._html, status_code=200)

        roster(
            team=Team.BOSTON_CELTICS,
            season_end_year=2026,
            output_type=OutputType.JSON,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )
        self.assertTrue(
            filecmp.cmp(
                self.output_file_path,
                self.expected_output_file_path))


class Test2026BostonRoster(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/teams/2026/BOS.html",
        ), 'r') as file_input: self._html = file_input.read();

    @requests_mock.Mocker()
    def test_length(self, m):
        m.get("https://www.basketball-reference.com/teams/BOS/2026.html", text=self._html, status_code=200)
        result = roster(season_end_year=2026, team=Team.BOSTON_CELTICS)
        self.assertEqual(len(result), 16)
        self.assertEqual(result[15], {"name": "Dalano Banton", "slug": "bantoda01", "number": "45",
                                      "position": Position.POINT_GUARD})


class Test2026PortlandRoster(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/teams/2026/POR.html",
        ), 'r') as file_input: self._html = file_input.read();

    @requests_mock.Mocker()
    def test_length(self, m):
        m.get("https://www.basketball-reference.com/teams/POR/2026.html", text=self._html, status_code=200)
        result = roster(season_end_year=2026, team=Team.PORTLAND_TRAIL_BLAZERS)
        self.assertEqual(len(result), 16)
        self.assertEqual(result[15], {"name": "Damian Lillard", "slug": "lillada01", "number": None,
                                      "position": Position.POINT_GUARD})


class Test1992ChicagoRoster(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/teams/1992/CHI.html",
        ), 'r') as file_input: self._html = file_input.read();

    @requests_mock.Mocker()
    def test_length(self, m):
        m.get("https://www.basketball-reference.com/teams/CHI/1992.html", text=self._html, status_code=200)
        result = roster(season_end_year=1992, team=Team.CHICAGO_BULLS)
        self.assertEqual(len(result), 16)
        self.assertEqual(result[-1], {"name": "Scott Williams", "slug": "willisc01", "number": "42",
                                      "position": Position.POWER_FORWARD})


class TestInvalidTeamSeason(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/teams/not_found.html",
        ), 'r') as file_input: self._html = file_input.read();

    @requests_mock.Mocker()
    def test_invalid_season(self, m):
        m.get("https://www.basketball-reference.com/teams/BOS/2026.html", text=self._html, status_code=404)
        self.assertRaisesRegex(InvalidTeamSeason, f'Team "Team.BOSTON_CELTICS" in 2026 is invalid',
                               roster,
                               season_end_year=2026,
                               team=Team.BOSTON_CELTICS)


class Test2001CharlotteHornetsRoster(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/teams/2001/CHH.html",
        ), 'r') as file_input: self._html = file_input.read();

    @requests_mock.Mocker()
    def test_length(self, m):
        m.get("https://www.basketball-reference.com/teams/CHH/2001.html", text=self._html, status_code=200)
        result = roster(season_end_year=2001, team=Team.CHARLOTTE_HORNETS)
        self.assertEqual(len(result), 16)
        self.assertEqual(result[-1], {"name": "David Wesley", "slug": "wesleda01", "number": "4",
                                      "position": Position.SHOOTING_GUARD})