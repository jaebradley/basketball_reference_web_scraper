import requests
from lxml import html

from basketball_reference_web_scraper.data import POSITION_ABBREVIATIONS_TO_POSITION
from basketball_reference_web_scraper.data import TEAM_TO_TEAM_ABBREVIATION, TEAM_ABBREVIATIONS_TO_TEAM, TeamTotal
from basketball_reference_web_scraper.errors import InvalidDate
from basketball_reference_web_scraper.html import PlayerSeasonTotalTable, BoxScoresPage
from basketball_reference_web_scraper.parser import PositionAbbreviationParser, TeamAbbreviationParser, \
    PlayerSeasonTotalsParser, TeamTotalsParser
from basketball_reference_web_scraper.parsers.box_scores.games import parse_game_url_paths
from basketball_reference_web_scraper.parsers.box_scores.players import parse_player_box_scores
from basketball_reference_web_scraper.parsers.play_by_play import parse_play_by_plays
from basketball_reference_web_scraper.parsers.players_advanced_season_totals import parse_players_advanced_season_totals
from basketball_reference_web_scraper.parsers.schedule import parse_schedule, parse_schedule_for_month_url_paths

BASE_URL = 'https://www.basketball-reference.com'


def player_box_scores(day, month, year):
    url = '{BASE_URL}/friv/dailyleaders.cgi?month={month}&day={day}&year={year}'.format(
        BASE_URL=BASE_URL,
        day=day,
        month=month,
        year=year
    )

    response = requests.get(url=url, allow_redirects=False)

    response.raise_for_status()

    if response.status_code == requests.codes.ok:
        return parse_player_box_scores(response.content)

    raise InvalidDate(day=day, month=month, year=year)


def schedule_for_month(url):
    response = requests.get(url=url)

    response.raise_for_status()

    return parse_schedule(response.content)


def season_schedule(season_end_year):
    url = '{BASE_URL}/leagues/NBA_{season_end_year}_games.html'.format(
        BASE_URL=BASE_URL,
        season_end_year=season_end_year
    )

    response = requests.get(url=url)

    response.raise_for_status()

    season_schedule_values = parse_schedule(response.content)
    other_month_url_paths = parse_schedule_for_month_url_paths(response.content)

    for month_url_path in other_month_url_paths:
        url = '{BASE_URL}{month_url_path}'.format(BASE_URL=BASE_URL, month_url_path=month_url_path)
        monthly_schedule = schedule_for_month(url=url)
        season_schedule_values.extend(monthly_schedule)

    return season_schedule_values


def players_season_totals(season_end_year):
    url = '{BASE_URL}/leagues/NBA_{season_end_year}_totals.html'.format(
        BASE_URL=BASE_URL,
        season_end_year=season_end_year,
    )

    response = requests.get(url=url)

    response.raise_for_status()

    table = PlayerSeasonTotalTable(html=html.fromstring(response.content))
    parser = PlayerSeasonTotalsParser(
        position_abbreviation_parser=PositionAbbreviationParser(
            abbreviations_to_positions=POSITION_ABBREVIATIONS_TO_POSITION
        ),
        team_abbreviation_parser=TeamAbbreviationParser(
            abbreviations_to_teams=TEAM_ABBREVIATIONS_TO_TEAM,
        )
    )
    return parser.parse(table.rows)


def players_advanced_season_totals(season_end_year):
    url = '{BASE_URL}/leagues/NBA_{season_end_year}_advanced.html'.format(
        BASE_URL=BASE_URL,
        season_end_year=season_end_year,
    )

    response = requests.get(url=url)

    response.raise_for_status()

    return parse_players_advanced_season_totals(response.content)


def team_box_score(game_url_path):
    url = "{BASE_URL}/{game_url_path}".format(BASE_URL=BASE_URL, game_url_path=game_url_path)

    response = requests.get(url=url)

    response.raise_for_status()

    page = BoxScoresPage(html.fromstring(response.content))
    combined_team_totals = [
        TeamTotal(team_abbreviation=table.team_abbreviation, totals=table.team_totals)
        for table in page.basic_statistics_tables
    ]
    parser = TeamTotalsParser(team_abbreviation_parser=TeamAbbreviationParser(
        abbreviations_to_teams=TEAM_ABBREVIATIONS_TO_TEAM,
    ))

    return parser.parse(combined_team_totals)


def team_box_scores(day, month, year):
    url = "{BASE_URL}/boxscores/".format(BASE_URL=BASE_URL)

    response = requests.get(url=url, params={"day": day, "month": month, "year": year})

    response.raise_for_status()

    game_url_paths = parse_game_url_paths(response.content)

    return [
        box_score
        for game_url_path in game_url_paths
        for box_score in team_box_score(game_url_path=game_url_path)
    ]


def play_by_play(home_team, day, month, year):

    add_0_if_needed = lambda s: "0" + s if len(s) == 1 else s

    # the hard-coded `0` in the url assumes we always take the first match of the given date and team.
    url = "{BASE_URL}/boxscores/pbp/{year}{month}{day}0{team_abbr}.html".format(
        BASE_URL=BASE_URL, year=year, month=add_0_if_needed(str(month)), day=add_0_if_needed(str(day)),
        team_abbr=TEAM_TO_TEAM_ABBREVIATION[home_team]
    )
    response = requests.get(url=url)
    response.raise_for_status()
    return parse_play_by_plays(response.content, home_team)
