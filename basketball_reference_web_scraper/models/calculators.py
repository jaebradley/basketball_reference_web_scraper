import datetime

from basketball_reference_web_scraper.data import TeamAbbreviation, Team, TEAM_ABBREVIATIONS_BY_TEAM

# The Charlotte Hornets' (with Basketball Reference abbreviation CHH) last game was May 15th, 2002
# https://www.basketball-reference.com/teams/CHH/2002_games.html
# The last season roster was the 2001-2002 season: https://www.basketball-reference.com/teams/CHH/2002.html
DATE_OF_CHARLOTTE_HORNETS_LAST_GAME = datetime.date(year=2002, month=5, day=15)


def calculate_team_abbreviation(team: Team, date: datetime.date) -> TeamAbbreviation:
    if team is Team.CHARLOTTE_HORNETS and date <= DATE_OF_CHARLOTTE_HORNETS_LAST_GAME:
        return TeamAbbreviation.CHH

    return TEAM_ABBREVIATIONS_BY_TEAM[team]


def calculate_team_abbreviation_from_team_and_season(team: Team, season_end_year: int) -> TeamAbbreviation:
    if team is Team.CHARLOTTE_HORNETS and season_end_year <= DATE_OF_CHARLOTTE_HORNETS_LAST_GAME.year:
        return TeamAbbreviation.CHH

    return TEAM_ABBREVIATIONS_BY_TEAM[team]
