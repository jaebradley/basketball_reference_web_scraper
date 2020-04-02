import requests
from lxml import html

from basketball_reference_web_scraper.errors import InvalidDate, InvalidPlayerAndSeason
from basketball_reference_web_scraper.html import DailyLeadersPage, PlayerSeasonBoxScoresPage, PlayerSeasonTotalTable


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

    def regular_season_player_box_scores(self, player_identifier, season_end_year):
        # Makes assumption that basketball reference pattern of breaking out player pathing using first character of
        # surname can be derived from the fact that basketball reference also has a pattern of player identifiers
        # starting with first few characters of player's surname
        url = '{BASE_URL}/players/{player_surname_starting_character}/{player_identifier}/gamelog/{season_end_year}' \
            .format(
                BASE_URL=HTTPService.BASE_URL,
                player_surname_starting_character=player_identifier[0],
                player_identifier=player_identifier,
                season_end_year=season_end_year,
            )

        response = requests.get(url=url, allow_redirects=False)
        response.raise_for_status()

        page = PlayerSeasonBoxScoresPage(html=html.fromstring(response.content))
        if page.regular_season_box_scores_table is None:
            raise InvalidPlayerAndSeason(player_identifier=player_identifier, season_end_year=season_end_year)

        return self.parser.parse_player_season_box_scores(box_scores=page.regular_season_box_scores_table.rows)

    def players_season_totals(self, season_end_year):
        url = '{BASE_URL}/leagues/NBA_{season_end_year}_totals.html'.format(
            BASE_URL=HTTPService.BASE_URL,
            season_end_year=season_end_year,
        )

        response = requests.get(url=url)

        response.raise_for_status()

        table = PlayerSeasonTotalTable(html=html.fromstring(response.content))
        return self.parser.parse_player_season_totals(totals=table.rows)
