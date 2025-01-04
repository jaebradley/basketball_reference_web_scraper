from basketball_reference_web_scraper.data import TeamAbbreviation, Team
from basketball_reference_web_scraper.models.teams import ABBREVIATIONS_BY_TEAM


def calculate_team_abbreviation(team: Team, season_end_year: int) -> TeamAbbreviation:
    if team is Team.CHARLOTTE_HORNETS and season_end_year <= 2002:
        return TeamAbbreviation.CHH

    return ABBREVIATIONS_BY_TEAM.get(team)
