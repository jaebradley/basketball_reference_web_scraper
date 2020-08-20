import requests
from lxml import html

from basketball_reference_web_scraper.data import TEAM_TO_TEAM_ABBREVIATION, TeamTotal, PlayerData
from basketball_reference_web_scraper.errors import InvalidDate, InvalidPlayerAndSeason
from basketball_reference_web_scraper.html import DailyLeadersPage, PlayerSeasonBoxScoresPage, PlayerSeasonTotalTable, \
    PlayerAdvancedSeasonTotalsTable, PlayByPlayPage, SchedulePage, BoxScoresPage, DailyBoxScoresPage, SearchPage, \
    PlayerPage, StandingsPage


class HTTPService:
    BASE_URL = 'https://www.basketball-reference.com'

    def __init__(self, parser):
        self.parser = parser

    def standings(self, season_end_year):
        url = '{BASE_URL}/leagues/NBA_{season_end_year}.html'.format(
            BASE_URL=HTTPService.BASE_URL,
            season_end_year=season_end_year,
        )

        response = requests.get(url=url, allow_redirects=False)

        response.raise_for_status()

        page = StandingsPage(html=html.fromstring(response.content))
        return self.parser.parse_division_standings(standings=page.division_standings.eastern_conference_table.rows) + \
               self.parser.parse_division_standings(standings=page.division_standings.western_conference_table.rows)

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

    def playoff_player_box_scores(self, player_identifier, season_end_year):
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
        if page.playoff_box_scores_table is None:
            raise InvalidPlayerAndSeason(player_identifier=player_identifier, season_end_year=season_end_year)

        return self.parser.parse_player_season_box_scores(box_scores=page.playoff_box_scores_table.rows)

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

    def schedule_for_month(self, url):
        response = requests.get(url=url)

        response.raise_for_status()

        page = SchedulePage(html=html.fromstring(html=response.content))
        return self.parser.parse_scheduled_games(games=page.rows)

    def season_schedule(self, season_end_year):
        url = '{BASE_URL}/leagues/NBA_{season_end_year}_games.html'.format(
            BASE_URL=HTTPService.BASE_URL,
            season_end_year=season_end_year
        )

        response = requests.get(url=url)

        response.raise_for_status()

        page = SchedulePage(html=html.fromstring(html=response.content))
        season_schedule_values = self.parser.parse_scheduled_games(games=page.rows)

        for month_url_path in page.other_months_schedule_urls:
            url = '{BASE_URL}{month_url_path}'.format(BASE_URL=HTTPService.BASE_URL, month_url_path=month_url_path)
            monthly_schedule = self.schedule_for_month(url=url)
            season_schedule_values.extend(monthly_schedule)

        return season_schedule_values

    def team_box_score(self, game_url_path):
        url = "{BASE_URL}/{game_url_path}".format(BASE_URL=HTTPService.BASE_URL, game_url_path=game_url_path)

        response = requests.get(url=url)

        response.raise_for_status()

        page = BoxScoresPage(html.fromstring(response.content))
        combined_team_totals = [
            TeamTotal(team_abbreviation=table.team_abbreviation, totals=table.team_totals)
            for table in page.basic_statistics_tables
        ]

        return self.parser.parse_team_totals(
            first_team_totals=combined_team_totals[0],
            second_team_totals=combined_team_totals[1],
        )

    def team_box_scores(self, day, month, year):
        url = "{BASE_URL}/boxscores/".format(BASE_URL=HTTPService.BASE_URL)

        response = requests.get(url=url, params={"day": day, "month": month, "year": year})

        response.raise_for_status()

        page = DailyBoxScoresPage(html=html.fromstring(response.content))

        return [
            box_score
            for game_url_path in page.game_url_paths
            for box_score in self.team_box_score(game_url_path=game_url_path)
        ]

    def search(self, term):
        response = requests.get(
            url="{BASE_URL}/search/search.fcgi".format(BASE_URL=HTTPService.BASE_URL),
            params={"search": term}
        )

        response.raise_for_status()

        player_results = []

        if response.url.startswith("{BASE_URL}/search/search.fcgi".format(BASE_URL=HTTPService.BASE_URL)):
            page = SearchPage(html=html.fromstring(response.content))
            parsed_results = self.parser.parse_player_search_results(nba_aba_baa_players=page.nba_aba_baa_players)
            player_results += parsed_results["players"]

            while page.nba_aba_baa_players_pagination_url is not None:
                response = requests.get(
                    url="{BASE_URL}/search/{pagination_url}".format(
                        BASE_URL=HTTPService.BASE_URL,
                        pagination_url=page.nba_aba_baa_players_pagination_url
                    )
                )

                response.raise_for_status()

                page = SearchPage(html=html.fromstring(response.content))

                parsed_results = self.parser.parse_player_search_results(nba_aba_baa_players=page.nba_aba_baa_players)
                player_results += parsed_results["players"]

        elif response.url.startswith("{BASE_URL}/players".format(BASE_URL=HTTPService.BASE_URL)):
            page = PlayerPage(html=html.fromstring(response.content))
            data = PlayerData(
                name=page.name,
                resource_location=response.url,
                league_abbreviations=set([
                    row.league_abbreviation
                    for row in page.totals_table.rows
                    if row.league_abbreviation is not None
                ])
            )
            player_results += [self.parser.parse_player_data(player=data)]

        return {
            "players": player_results
        }
