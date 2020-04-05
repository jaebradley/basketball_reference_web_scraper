import requests
from lxml import html

from basketball_reference_web_scraper.data import TEAM_TO_TEAM_ABBREVIATION
from basketball_reference_web_scraper.errors import InvalidDate, InvalidPlayerAndSeason
from basketball_reference_web_scraper.html import DailyLeadersPage, PlayerSeasonBoxScoresPage, PlayerSeasonTotalTable, \
    PlayerAdvancedSeasonTotalsTable, PlayByPlayPage


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

    def play_by_play(self, home_team, day, month, year):
        add_0_if_needed = lambda s: "0" + s if len(s) == 1 else s

        # the hard-coded `0` in the url assumes we always take the first match of the given date and team.
        url = "{BASE_URL}/boxscores/pbp/{year}{month}{day}0{team_abbr}.html".format(
            BASE_URL=HTTPService.BASE_URL, year=year, month=add_0_if_needed(str(month)), day=add_0_if_needed(str(day)),
            team_abbr=TEAM_TO_TEAM_ABBREVIATION[home_team]
        )
        response = requests.get(url=url)
        response.raise_for_status()

        page = PlayByPlayPage(html=html.fromstring(response.content))

        return self.parser.parse_play_by_plays(
            play_by_plays=page.play_by_play_table.rows,
            away_team_name=page.away_team_name,
            home_team_name=page.home_team_name,
        )

    def players_advanced_season_totals(self, season_end_year, include_combined_values=False):
        url = '{BASE_URL}/leagues/NBA_{season_end_year}_advanced.html'.format(
            BASE_URL=HTTPService.BASE_URL,
            season_end_year=season_end_year,
        )

        response = requests.get(url=url)

        response.raise_for_status()

        table = PlayerAdvancedSeasonTotalsTable(html=html.fromstring(response.content))
        return self.parser.parse_player_advanced_season_totals_parser(totals=table.get_rows(include_combined_values))

    def players_season_totals(self, season_end_year):
        url = '{BASE_URL}/leagues/NBA_{season_end_year}_totals.html'.format(
            BASE_URL=HTTPService.BASE_URL,
            season_end_year=season_end_year,
        )

        response = requests.get(url=url)

        response.raise_for_status()

        table = PlayerSeasonTotalTable(html=html.fromstring(response.content))
        return self.parser.parse_player_season_totals(totals=table.rows)
