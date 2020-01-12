import requests
import unicodedata

from basketball_reference_web_scraper.data import TEAM_TO_TEAM_ABBREVIATION
from basketball_reference_web_scraper.errors import InvalidDate
from basketball_reference_web_scraper.parsers.box_scores.games import parse_game_url_paths
from basketball_reference_web_scraper.parsers.box_scores.players import parse_player_box_scores
from basketball_reference_web_scraper.parsers.box_scores.teams import parse_team_totals
from basketball_reference_web_scraper.parsers.play_by_play import parse_play_by_plays
from basketball_reference_web_scraper.parsers.player_number import parse_player_link, parse_player_number
from basketball_reference_web_scraper.parsers.players_advanced_season_totals import parse_players_advanced_season_totals
from basketball_reference_web_scraper.parsers.players_season_totals import parse_players_season_totals
from basketball_reference_web_scraper.parsers.schedule import parse_schedule, parse_schedule_for_month_url_paths

BASE_URL = 'https://www.basketball-reference.com'


def player_box_scores(day, month, year):
    url = f'{BASE_URL}/friv/dailyleaders.cgi?month={month}&day={day}&year={year}'

    response = requests.get(url=url, allow_redirects=False)

    response.raise_for_status()

    if response.status_code == requests.codes.ok:
        box_scores = parse_player_box_scores(response.content)
        # for player in box_scores:
        #     num = player_number(player['name'])
        #     player['jersey_number'] = num

        return box_scores

    raise InvalidDate(day=day, month=month, year=year)


def schedule_for_month(url):
    response = requests.get(url=url)

    response.raise_for_status()

    return parse_schedule(response.content)


def season_schedule(season_end_year):
    url = f'{BASE_URL}/leagues/NBA_{season_end_year}_games.html'

    response = requests.get(url=url)

    response.raise_for_status()

    season_schedule_values = parse_schedule(response.content)
    other_month_url_paths = parse_schedule_for_month_url_paths(response.content)

    for month_url_path in other_month_url_paths:
        url = f'{BASE_URL}{month_url_path}'
        monthly_schedule = schedule_for_month(url=url)
        season_schedule_values.extend(monthly_schedule)

    return season_schedule_values


def players_season_totals(season_end_year):
    url = f'{BASE_URL}/leagues/NBA_{season_end_year}_totals.html'

    response = requests.get(url=url)

    response.raise_for_status()

    return parse_players_season_totals(response.content)


def player_number(player_name):
    last_initial = player_name.split()[1][0].lower()
    last_initial = unicodedata.normalize('NFD', last_initial) \
        .encode('ascii', 'ignore') \
        .decode("utf-8")

    url = f'{BASE_URL}/players/{last_initial}/'

    response = requests.get(url=url)
    response.raise_for_status()

    ext = parse_player_link(player_name, response.content)

    url = url + ext + '.html'
    response = requests.get(url=url)

    response.raise_for_status()

    return parse_player_number(response.content)


def players_advanced_season_totals(season_end_year):
    url = f'{BASE_URL}/leagues/NBA_{season_end_year}_advanced.html'

    response = requests.get(url=url)

    response.raise_for_status()

    return parse_players_advanced_season_totals(response.content)


def team_box_score(game_url_path):
    url = f"{BASE_URL}/{game_url_path}"

    response = requests.get(url=url)

    response.raise_for_status()

    return parse_team_totals(response.content)


def team_box_scores(day, month, year):
    url = f"{BASE_URL}/boxscores/"

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
    url = f"{BASE_URL}/boxscores/pbp/{year}{add_0_if_needed(str(month))}{add_0_if_needed(str(day))}\
    0{TEAM_TO_TEAM_ABBREVIATION[home_team]}.html"
    response = requests.get(url=url)
    response.raise_for_status()
    return parse_play_by_plays(response.content, home_team)
