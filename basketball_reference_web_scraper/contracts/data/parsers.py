from datetime import datetime
from typing import Dict

from coverage.types import Protocol
from price_parser import Price

from basketball_reference_web_scraper.contracts.data.models import Salary, PlayerContract, Player
from basketball_reference_web_scraper.contracts.page.parsers import PlayerRowData, PlayerContractData
from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM

GUARANTEED_SALARY_COLUMN_DATA_STAT_VALUE = "remain_gtd"


class PlayerContractRowDataProcessor(Protocol):
    def process_row(self, headers: Dict[str, str], row_data: PlayerRowData) -> PlayerContract:
        raise NotImplementedError()


def parse_season_start_date(serialized_season: str) -> int:
    return datetime.strptime(serialized_season, "%Y-%y").year


def parse_player_contract_values(contract_values_by_column_identifier: Dict[str, str],
                                 column_names_by_identifier: Dict[str, str]):
    guaranteed_salary_value = contract_values_by_column_identifier.get(GUARANTEED_SALARY_COLUMN_DATA_STAT_VALUE, None)
    if guaranteed_salary_value:
        parsed_guaranteed_salary = Price.fromstring(price=guaranteed_salary_value)

        return (
            dict(map(lambda item: (
                item[0], None if item[1] is None else Salary(amount=item[1].amount, currency=item[1].currency)),
                     map(lambda item: (item[0], None if item[1] is None else Price.fromstring(item[1])),
                         map(lambda item: (parse_season_start_date(item[0]), item[1]),
                             map(lambda item: (column_names_by_identifier.get(item[0]), item[1]),
                                 filter(lambda item: item[0] != GUARANTEED_SALARY_COLUMN_DATA_STAT_VALUE,
                                        contract_values_by_column_identifier.items())))))),
            Salary(
                amount=parsed_guaranteed_salary.amount,
                currency=parsed_guaranteed_salary.currency
            ))

    raise ValueError("Unparseable player contract values")


def create_player_contract(player_contract_data: PlayerContractData):
    salaries_by_season, guaranteed_salary = parse_player_contract_values(
        contract_values_by_column_identifier=player_contract_data.row.values_by_header,
        column_names_by_identifier=player_contract_data.headers
    )

    return PlayerContract(
        player=Player(
            identifier=player_contract_data.row.id,
            name=player_contract_data.row.name
        ),
        team=TEAM_ABBREVIATIONS_TO_TEAM.get(player_contract_data.row.team_abbreviation, None),
        salaries_by_season_start_year=salaries_by_season,
        guaranteed_salary=guaranteed_salary
    )
