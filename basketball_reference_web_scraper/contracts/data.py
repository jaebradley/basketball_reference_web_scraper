import dataclasses
import enum
from typing import Optional, Dict


@dataclasses.dataclass(frozen=True)
class PlayerData:
    name: str
    identifier: str


class SalaryOption(enum.Enum):
    PLAYER = "player"
    TEAM = "team"


@dataclasses.dataclass(frozen=True)
class SeasonSalaryData:
    value: str
    season_identifier: str
    option: Optional[SalaryOption]


@dataclasses.dataclass(frozen=True)
class RowData:
    player: Optional[PlayerData]
    team_id: Optional[str]
    salary_by_season: Dict[str, Optional[SeasonSalaryData]]
