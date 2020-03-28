import requests
from lxml import html

from basketball_reference_web_scraper.errors import InvalidDate
from basketball_reference_web_scraper.html import DailyLeadersPage


class HTTPService:
    BASE_URL = 'https://www.basketball-reference.com'

    def __init__(self, parser):
        self.parser = parser

    def player_box_scores(self, day, month, year):
        url = '{BASE_URL}/friv/dailyleaders.cgi?month={month}&day={day}&year={year}'.format(
            BASE_URL=HTTPService.BASE_URL,
            day=day,
            month=month,
            year=year
        )

        response = requests.get(url=url, allow_redirects=False)

        response.raise_for_status()

        if response.status_code == requests.codes.ok:
            page = DailyLeadersPage(html=html.fromstring(response.content))
            return self.parser.parse_player_box_scores(box_scores=page.daily_leaders)

        raise InvalidDate(day=day, month=month, year=year)