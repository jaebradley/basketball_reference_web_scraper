import datetime

from basketball_reference_web_scraper.data import TeamAbbreviation, Team
from basketball_reference_web_scraper.models.teams import ABBREVIATIONS_BY_TEAM

# The Charlotte Hornets' (with Basketball Reference abbreviation CHH) last game was May 15th, 2002
# https://www.basketball-reference.com/teams/CHH/2002_games.html
DATE_OF_CHARLOTTE_HORNETS_LAST_GAME = datetime.date(year=2002, month=5, day=15)


def calculate_team_abbreviation(team: Team, date: datetime.date) -> TeamAbbreviation:
    if team is Team.CHARLOTTE_HORNETS and date <= DATE_OF_CHARLOTTE_HORNETS_LAST_GAME:
        return TeamAbbreviation.CHH

    return ABBREVIATIONS_BY_TEAM.get(team)
