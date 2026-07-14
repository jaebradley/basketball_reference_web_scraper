import dataclasses
import datetime

from basketball_reference_web_scraper.data import TeamAbbreviation


@dataclasses.dataclass(frozen=True)
class PlayByPlayURLData:
    date: datetime.date
    team_abbreviation: TeamAbbreviation
