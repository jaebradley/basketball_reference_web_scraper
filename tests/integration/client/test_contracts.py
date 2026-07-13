import os
from decimal import Decimal
from unittest import TestCase

import requests_mock
from basketball_reference_web_scraper.contracts.data.models import Contract, Player, Salary
from client import contracts
from basketball_reference_web_scraper.data import Team


class TestContracts(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/contracts/2026/07/12.html"
        ), 'r') as file_input: self._html = file_input.read()

    @requests_mock.Mocker()
    def test_contracts(self, m):
        m.get("https://www.basketball-reference.com/contracts/players.html",
              text=self._html,
              status_code=200)
        data = []
        contracts(contract_processor=data.append)
        self.assertEqual(416, len(data))
        self.assertEqual(Contract(
            player=Player(identifier="curryst01", name="Stephen Curry"),
            team=Team.GOLDEN_STATE_WARRIORS,
            salaries_by_season_start_year={
                2026: Salary(Decimal(62587158)),
                2027: None,
                2028: None,
                2029: None,
                2030: None,
                2031: None,
            },
            remaining_guaranteed_salary=Salary(Decimal(62587158))
        ), data[0])

        self.assertEqual(Contract(
            player=Player(identifier="hardeja01", name="James Harden"),
            team=Team.CLEVELAND_CAVALIERS,
            salaries_by_season_start_year={
                2026: Salary(Decimal(42317307)),
                2027: None,
                2028: None,
                2029: None,
                2030: None,
                2031: None,
            },
            remaining_guaranteed_salary=None
        ), data[29])

        self.assertEqual(Contract(
            player=Player(identifier="louzama01", name="Didi Louzada"),
            team=Team.PORTLAND_TRAIL_BLAZERS,
            salaries_by_season_start_year={
                2026: Salary(Decimal(268032)),
                2027: Salary(Decimal(268032)),
                2028: Salary(Decimal(268032)),
                2029: None,
                2030: None,
                2031: None,
            },
            remaining_guaranteed_salary=Salary(Decimal(804096))
        ), data[415])
