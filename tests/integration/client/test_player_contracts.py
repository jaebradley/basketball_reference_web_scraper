import os
from unittest import TestCase

import requests_mock

from basketball_reference_web_scraper.client import player_contracts


class TestPlayerContracts(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/contracts/2025/03/07.html"
        ), 'r') as file_input: self._html = file_input.read()

    @requests_mock.Mocker()
    def test_player_contracts(self, m):
        m.get("https://www.basketball-reference.com/contracts/players.html",
              text=self._html,
              status_code=200)
        data = []
        player_contracts(player_contract_processor=lambda player_contract: data.append(player_contract))
        assert 496 == len(data)
