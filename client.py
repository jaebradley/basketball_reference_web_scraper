import requests

from parsers.box_scores import parse_box_score

BASE_URL = 'http://www.basketball-reference.com'


def get_box_scores(day, month, year):
    url = '{BASE_URL}/friv/dailyleaders.cgi?month={month}&day={day}&year={year}'.format(
        BASE_URL=BASE_URL,
        day=day,
        month=month,
        year=year
    )

    response = requests.get(url=url)

    response.raise_for_status()

    return parse_box_score(response.content)
