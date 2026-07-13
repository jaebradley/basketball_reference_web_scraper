import os
from decimal import Decimal
from unittest import TestCase

from basketball_reference_web_scraper.contracts.data.models import Player, PlayerContract, Salary
from basketball_reference_web_scraper.contracts.data.parsers import PlayerContractParser, SalariesBySeasonParser, \
    deserialize_season_start_year, \
    deserialize_optional_salary, deserialize_guaranteed_salary, deserialize_team
from basketball_reference_web_scraper.contracts.page.parsers import NothingMoreToParse
from basketball_reference_web_scraper.contracts.page.parsers import PlayerContractsPageParser, PlayerContractData
from basketball_reference_web_scraper.data import Team


class TestParseContractsPage(TestCase):
    def setUp(self):
        super().setUp()

        self.player_contract_parser = PlayerContractParser(
            salary_generator=SalariesBySeasonParser(season_start_year_deserializer=deserialize_season_start_year,
                                                    salary_deserializer=deserialize_optional_salary),
            guaranteed_salary_generator=deserialize_guaranteed_salary,
            player_generator=lambda row: Player(identifier=row.id, name=row.name),
            team_generator=deserialize_team,
        )

    def test_parsing_contracts_on_20260712(self):
        contracts = []

        def extract_table_data(row: PlayerContractData) -> PlayerContract:
            parsed_row = self.player_contract_parser.parse_table_data(data=row)
            contracts.append(parsed_row)
            return parsed_row

        with open(os.path.join(
                os.path.dirname(__file__),
                f"../../files/contracts/2026/07/12.html",
        ), 'r') as file_input:
            with PlayerContractsPageParser(extract_table_data) as p:
                # Minimum possible chunk at a time for testing
                while chunk := file_input.read(1):
                    try:
                        p.parse(chunk=chunk)
                    except NothingMoreToParse:
                        break

        self.assertEqual(416, len(contracts))
        self.assertEqual(PlayerContract(
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
        ), contracts[0])

        self.assertEqual(PlayerContract(
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
        ), contracts[29])

        self.assertEqual(PlayerContract(
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
        ), contracts[415])
