import requests

from errors import InvalidDate
from parsers.box_scores import parse_box_score
from parsers.schedule import parse_schedule, parse_schedule_for_month_url_paths

BASE_URL = 'https://www.basketball-reference.com'


def box_scores(day, month, year):
    url = '{BASE_URL}/friv/dailyleaders.cgi?month={month}&day={day}&year={year}'.format(
        BASE_URL=BASE_URL,
        day=day,
        month=month,
        year=year
    )

    response = requests.get(url=url, allow_redirects=False)

    if 200 <= response.status_code < 300:
        return parse_box_score(response.content)

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

    season_schedule = parse_schedule(response.content)
    other_month_url_paths = parse_schedule_for_month_url_paths(response.content)

    for month_url_path in other_month_url_paths:
        url = '{BASE_URL}{month_url_path}'.format(BASE_URL=BASE_URL, month_url_path=month_url_path)
        schedule_for_month = schedule_for_month(url=url)
        season_schedule.extend(schedule_for_month)

    return season_schedule
