from dataclasses import dataclass
from decimal import Decimal
from locale import currency
from typing import Dict, Optional

from basketball_reference_web_scraper.data import Team


@dataclass(frozen=True)
class Player:
    identifier: str
    name: str

    def __post_init__(self):
        if 0 == len(self.identifier):
            raise ValueError("identifier should not be an empty string")

        if 0 == len(self.name):
            raise ValueError("name should not be an empty string")

        if any(char.isspace() for char in self.identifier):
            raise ValueError(f"identifier: {self.identifier} should not contain whitespace")


@dataclass(frozen=True)
class Salary:
    amount_in_usd: Decimal

    def __post_init__(self):
        if self.amount_in_usd is None:
            raise ValueError("amount should not be None")

        if 0 > self.amount_in_usd:
            raise ValueError("amount should not be negative")


@dataclass(frozen=True)
class PlayerContract:
    player: Player
    team: Team
    salaries_by_season_start_year: Dict[int, Optional[Salary]]
    remaining_guaranteed_salary: Optional[Salary]

    def __post_init__(self):
        if self.player is None:
            raise ValueError("player should not be None")

        if self.team is None:
            raise ValueError("team should not be None")

        if self.salaries_by_season_start_year is None:
            raise ValueError("season salaries should not be None")

        if 0 == len(self.salaries_by_season_start_year):
            raise ValueError("season salaries should not be empty")

        if all(salary is None for salary in self.salaries_by_season_start_year.values()):
            raise ValueError("not all salaries should be None")
