from datetime import datetime
from typing import Dict, Optional

from price_parser import Price

from basketball_reference_web_scraper.contracts.data.models import Salary, PlayerContract, Player
from basketball_reference_web_scraper.contracts.page.parsers import PlayerContractData as PlayerContractTableData, \
    PlayerRowData
from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM, Team

GUARANTEED_SALARY_COLUMN_DATA_STAT_VALUE = "remain_gtd"

from typing import Callable


class SalariesBySeasonParser:
    def __init__(self, season_start_year_deserializer: Callable[[str], int],
                 salary_deserializer: Callable[[Optional[str]], Optional[Salary]]):
        self._season_start_year_deserializer = season_start_year_deserializer
        self._salary_deserializer = salary_deserializer

    def parse(self, contract_values_by_column_identifier: Dict[str, str],
              column_names_by_identifier: Dict[str, str]) -> Dict[int, Optional[Salary]]:
        return dict(
            map(lambda item: (item[0], self._salary_deserializer(item[1])),
                map(lambda column_name_and_value: (
                    self._season_start_year_deserializer(column_name_and_value[0]), column_name_and_value[1]),
                    map(
                        lambda season_salary_columns_by_value: (
                            column_names_by_identifier[season_salary_columns_by_value[0]],
                            season_salary_columns_by_value[1]),
                        filter(lambda value_by_identifier: value_by_identifier[
                                                               0] != GUARANTEED_SALARY_COLUMN_DATA_STAT_VALUE,
                               contract_values_by_column_identifier.items())))))


def deserialize_season_start_year(serialized_season: str) -> int:
    """
    Parses the season strings for each contract year column. These strings have a form like "2024-25"
    :param serialized_season: str representing the column name of a particular contract year season
    :return: int representing the starting year for a given contract season
    """
    return datetime.strptime(serialized_season.split("-")[0], "%Y").year


def deserialize_optional_salary(salary: Optional[str]) -> Optional[Salary]:
    if salary:
        parsed_amount = Price.fromstring(salary)
        return Salary(amount=parsed_amount.amount, currency=parsed_amount.currency)


def deserialize_team(abbreviation: str) -> Team:
    team = TEAM_ABBREVIATIONS_TO_TEAM.get(abbreviation, None)
    if team:
        return team

    raise ValueError(f"Unable to deserialize team abbreviation: {abbreviation}")


def deserialize_guaranteed_salary(contract_values_by_column_identifier: Dict[str, str]) -> Salary:
    guaranteed_salary_value = deserialize_optional_salary(
        contract_values_by_column_identifier.get(
            GUARANTEED_SALARY_COLUMN_DATA_STAT_VALUE, None
        )
    )
    if guaranteed_salary_value:
        return guaranteed_salary_value

    raise ValueError(
        f"Could not identify guaranteed salary value in header values: {contract_values_by_column_identifier}")


class PlayerContractParser:
    def __init__(self,
                 salary_generator: SalariesBySeasonParser,
                 guaranteed_salary_generator: Callable[[Dict[str, Optional[str]]], Salary],
                 player_generator: Callable[[PlayerRowData], Player],
                 team_generator: Callable[[str], Team]):
        self.salary_generator = salary_generator
        self.guaranteed_salary_generator = guaranteed_salary_generator
        self.player_generator = player_generator
        self.team_generator = team_generator

    def parse_table_data(self, data: PlayerContractTableData) -> PlayerContract:
        return PlayerContract(
            player=self.player_generator(data.row),
            team=self.team_generator(data.row.team_abbreviation),
            salaries_by_season_start_year=self.salary_generator.parse(data.row.values_by_header, data.headers),
            guaranteed_salary=self.guaranteed_salary_generator(data.row.values_by_header)
        )
