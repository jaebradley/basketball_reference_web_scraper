import datetime
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable
from urllib.parse import urljoin

import requests
from basketball_reference_web_scraper.contracts.data.models import Contract
from basketball_reference_web_scraper.contracts.page.parsers import (
    PlayerContractsPageParser,
    NothingMoreToParse,
    ContractRowData,
)
from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_BY_TEAM
from basketball_reference_web_scraper.data import TeamTotal, PlayerData
from basketball_reference_web_scraper.errors import CouldNotGetPlayerContractData
from basketball_reference_web_scraper.errors import InvalidDate, InvalidPlayerAndSeason
from basketball_reference_web_scraper.html import (
    DailyLeadersPage,
    PlayerSeasonBoxScoresPage,
    PlayerSeasonTotalTable,
    PlayerAdvancedSeasonTotalsTable,
    PlayByPlayPage,
    SchedulePage,
    BoxScoresPage,
    DailyBoxScoresPage,
    SearchPage,
    PlayerPage,
    StandingsPage,
)
from basketball_reference_web_scraper.models.calculators import (
    calculate_team_abbreviation,
    calculate_team_abbreviation_from_team_and_season,
)
from basketball_reference_web_scraper.serialization.urls.models import PlayByPlayURLData
from basketball_reference_web_scraper.serialization.urls.serializers import (
    DEFAULT_PLAY_BY_PLAY_URL_SERIALIZER,
)
from basketball_reference_web_scraper.shooting.html import (
    PlayersSeasonShootingStatisticsTable,
)
from basketball_reference_web_scraper.team_season.html import TeamSeasonPage
from lxml import html

# Default sessions are shared per thread so sequential client calls create
# several HTTPService instances but still reuse one connection pool.
_DEFAULT_SESSIONS = threading.local()


def _default_session():
    session = getattr(_DEFAULT_SESSIONS, "session", None)
    if session is None:
        session = requests.Session()
        _DEFAULT_SESSIONS.session = session
    return session


class HTTPService:
    BASE_URL = "https://www.basketball-reference.com"
    DEFAULT_REQUEST_TIMEOUT_SECONDS = 30

    def __init__(self, parser, session_factory=None):
        self.parser = parser
        self._session_factory = session_factory
        self._sessions = threading.local()

    @property
    def session(self):
        if self._session_factory is None:
            # Sequential client calls in one thread share this pool.
            return _default_session()
        # A custom factory is isolated per service and per thread, which keeps
        # tests and embedders from sharing connection state.
        session = getattr(self._sessions, "session", None)
        if session is None:
            session = self._session_factory()
            self._sessions.session = session
        return session

    def _map(self, function, items, max_workers):
        values = list(items)
        if max_workers is None or max_workers < 1:
            raise ValueError("max_workers must be at least 1")
        if max_workers == 1 or len(values) <= 1:
            return [function(value) for value in values]
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            return list(executor.map(function, values))

    def standings(self, season_end_year):
        url = "{BASE_URL}/leagues/NBA_{season_end_year}.html".format(
            BASE_URL=HTTPService.BASE_URL,
            season_end_year=season_end_year,
        )

        response = self.session.get(
            url=url,
            allow_redirects=False,
            timeout=HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS,
        )

        response.raise_for_status()

        if response.status_code != requests.codes.ok:
            raise requests.exceptions.HTTPError(
                "{status_code} response for url: {url}".format(
                    status_code=response.status_code, url=url
                ),
                response=response,
            )

        page = StandingsPage(html=html.fromstring(response.content))
        return self.parser.parse_division_standings(
            standings=page.division_standings.eastern_conference_table.rows
        ) + self.parser.parse_division_standings(
            standings=page.division_standings.western_conference_table.rows
        )

    def player_box_scores(self, day, month, year):
        try:
            datetime.date(year=year, month=month, day=day)
        except (ValueError, TypeError):
            raise InvalidDate(day=day, month=month, year=year)

        url = "{BASE_URL}/friv/dailyleaders.cgi?month={month}&day={day}&year={year}".format(
            BASE_URL=HTTPService.BASE_URL, day=day, month=month, year=year
        )

        response = self.session.get(
            url=url,
            allow_redirects=False,
            timeout=HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS,
        )

        response.raise_for_status()

        if response.status_code == requests.codes.ok:
            page = DailyLeadersPage(html=html.fromstring(response.content))
            return self.parser.parse_player_box_scores(box_scores=page.daily_leaders)

        raise InvalidDate(day=day, month=month, year=year)

    def regular_season_player_box_scores(
        self, player_identifier, season_end_year, include_inactive_games=False
    ):
        if player_identifier is None or len(player_identifier) == 0:
            raise InvalidPlayerAndSeason(
                player_identifier=player_identifier, season_end_year=season_end_year
            )
        # Makes assumption that basketball reference pattern of breaking out player pathing using first character of
        # surname can be derived from the fact that basketball reference also has a pattern of player identifiers
        # starting with first few characters of player's surname
        url = "{BASE_URL}/players/{player_surname_starting_character}/{player_identifier}/gamelog/{season_end_year}".format(
            BASE_URL=HTTPService.BASE_URL,
            player_surname_starting_character=player_identifier[0],
            player_identifier=player_identifier,
            season_end_year=season_end_year,
        )

        response = self.session.get(
            url=url,
            allow_redirects=False,
            timeout=HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()

        page = PlayerSeasonBoxScoresPage(html=html.fromstring(response.content))
        if page.regular_season_box_scores_table is None:
            raise InvalidPlayerAndSeason(
                player_identifier=player_identifier, season_end_year=season_end_year
            )

        return self.parser.parse_player_season_box_scores(
            box_scores=page.regular_season_box_scores_table.rows,
            include_inactive_games=include_inactive_games,
            player_identifier=player_identifier,
        )

    def playoff_player_box_scores(
        self, player_identifier, season_end_year, include_inactive_games=False
    ):
        if player_identifier is None or len(player_identifier) == 0:
            raise InvalidPlayerAndSeason(
                player_identifier=player_identifier, season_end_year=season_end_year
            )
        # Makes assumption that basketball reference pattern of breaking out player pathing using first character of
        # surname can be derived from the fact that basketball reference also has a pattern of player identifiers
        # starting with first few characters of player's surname
        url = "{BASE_URL}/players/{player_surname_starting_character}/{player_identifier}/gamelog/{season_end_year}".format(
            BASE_URL=HTTPService.BASE_URL,
            player_surname_starting_character=player_identifier[0],
            player_identifier=player_identifier,
            season_end_year=season_end_year,
        )

        response = self.session.get(
            url=url,
            allow_redirects=False,
            timeout=HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()

        page = PlayerSeasonBoxScoresPage(html=html.fromstring(response.content))
        if page.playoff_box_scores_table is None:
            raise InvalidPlayerAndSeason(
                player_identifier=player_identifier, season_end_year=season_end_year
            )

        return self.parser.parse_player_season_box_scores(
            box_scores=page.playoff_box_scores_table.rows,
            include_inactive_games=include_inactive_games,
            player_identifier=player_identifier,
        )

    def play_by_play(self, home_team, day, month, year):
        try:
            date = datetime.date(year=year, month=month, day=day)
        except (ValueError, TypeError):
            raise InvalidDate(day=day, month=month, year=year)
        url = DEFAULT_PLAY_BY_PLAY_URL_SERIALIZER.serialize(
            value=PlayByPlayURLData(
                date=date,
                team_abbreviation=calculate_team_abbreviation(
                    team=home_team, date=date
                ),
            )
        )
        response = self.session.get(
            url=url, timeout=HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()

        page = PlayByPlayPage(html=html.fromstring(response.content))

        return self.parser.parse_play_by_plays(
            play_by_plays=page.play_by_play_table.rows,
            away_team_name=page.away_team_name,
            home_team_name=page.home_team_name,
        )

    def players_advanced_season_totals(
        self, season_end_year, include_combined_values=False
    ):
        url = "{BASE_URL}/leagues/NBA_{season_end_year}_advanced.html".format(
            BASE_URL=HTTPService.BASE_URL,
            season_end_year=season_end_year,
        )

        response = self.session.get(
            url=url, timeout=HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS
        )

        response.raise_for_status()

        table = PlayerAdvancedSeasonTotalsTable(html=html.fromstring(response.content))
        return self.parser.parse_player_advanced_season_totals_parser(
            totals=table.get_rows(include_combined_values)
        )

    def players_season_totals(self, season_end_year):
        url = "{BASE_URL}/leagues/NBA_{season_end_year}_totals.html".format(
            BASE_URL=HTTPService.BASE_URL,
            season_end_year=season_end_year,
        )

        response = self.session.get(
            url=url, timeout=HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS
        )

        response.raise_for_status()

        table = PlayerSeasonTotalTable(html=html.fromstring(response.content))
        return self.parser.parse_player_season_totals(totals=table.rows)

    def players_season_shooting_statistics(self, season_end_year):
        url = "{BASE_URL}/leagues/NBA_{season_end_year}_shooting.html".format(
            BASE_URL=HTTPService.BASE_URL,
            season_end_year=season_end_year,
        )
        response = self.session.get(
            url=url, timeout=HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS
        )

        response.raise_for_status()
        table = PlayersSeasonShootingStatisticsTable(
            html=html.fromstring(response.content)
        )
        return self.parser.parse_player_season_shooting_statistics(totals=table.rows)

    def schedule_for_month(self, url):
        response = self.session.get(
            url=url, timeout=HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS
        )

        response.raise_for_status()

        page = SchedulePage(html=html.fromstring(html=response.content))
        return self.parser.parse_scheduled_games(games=page.rows)

    def season_schedule(self, season_end_year, max_workers=1):
        url = "{BASE_URL}/leagues/NBA_{season_end_year}_games.html".format(
            BASE_URL=HTTPService.BASE_URL, season_end_year=season_end_year
        )

        response = self.session.get(
            url=url, timeout=HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS
        )

        response.raise_for_status()

        page = SchedulePage(html=html.fromstring(html=response.content))
        season_schedule_values = self.parser.parse_scheduled_games(games=page.rows)

        month_urls = [
            "{BASE_URL}{month_url_path}".format(
                BASE_URL=HTTPService.BASE_URL, month_url_path=month_url_path
            )
            for month_url_path in page.other_months_schedule_urls
        ]
        # executor.map preserves the page order, so concurrent output is
        # identical to the sequential result.
        for monthly_schedule in self._map(
            self.schedule_for_month, month_urls, max_workers
        ):
            season_schedule_values.extend(monthly_schedule)

        return season_schedule_values

    def team_box_score(self, game_url_path):
        url = "{BASE_URL}/{game_url_path}".format(
            BASE_URL=HTTPService.BASE_URL, game_url_path=game_url_path
        )

        response = self.session.get(
            url=url, timeout=HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS
        )

        response.raise_for_status()

        page = BoxScoresPage(html.fromstring(response.content))
        tables = page.statistics_tables
        # Use batched when the minimum python version supported is 3.12 (https://docs.python.org/3/library/itertools.html#itertools.batched)
        paired_basic_and_advanced_tables = list(zip(tables[::2], tables[1::2]))
        # TODO @jaebradley: This logic is pretty messy. There's gotta be a better way of determining first/second team (perhaps via the game URL path). Additionally, a Mapping feels like the most natural way of representing the statistics tables.
        combined_team_totals = list(
            map(
                lambda paired_tables: TeamTotal(
                    basic_statistics_table=paired_tables[0],
                    advanced_statistics_table=paired_tables[1],
                ),
                paired_basic_and_advanced_tables,
            )
        )

        if len(combined_team_totals) != 2:
            raise ValueError(
                "Expected 2 teams' worth of statistics tables for game at {game_url_path} but found {combined_team_totals_count}".format(
                    game_url_path=game_url_path,
                    combined_team_totals_count=len(combined_team_totals),
                )
            )

        return self.parser.parse_team_totals(
            first_team_totals=combined_team_totals[0],
            second_team_totals=combined_team_totals[1],
        )

    def team_box_scores(self, day, month, year, max_workers=1):
        try:
            datetime.date(year=year, month=month, day=day)
        except (ValueError, TypeError):
            raise InvalidDate(day=day, month=month, year=year)

        url = "{BASE_URL}/boxscores/".format(BASE_URL=HTTPService.BASE_URL)

        response = self.session.get(
            url=url,
            params={"day": day, "month": month, "year": year},
            timeout=HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS,
        )

        response.raise_for_status()

        page = DailyBoxScoresPage(html=html.fromstring(response.content))
        game_box_scores = self._map(
            self.team_box_score, page.game_url_paths, max_workers
        )

        return [box_score for game in game_box_scores for box_score in game]

    def roster(self, team, season_end_year):
        url = "{BASE_URL}/teams/{team_abbreviation}/{season_end_year}.html".format(
            BASE_URL=HTTPService.BASE_URL,
            team_abbreviation=calculate_team_abbreviation_from_team_and_season(
                team=team, season_end_year=season_end_year
            ).value,
            season_end_year=season_end_year,
        )

        response = self.session.get(
            url=url, timeout=HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS
        )

        response.raise_for_status()

        return self.parser.parse_roster_data(
            team_season_page=TeamSeasonPage(html=html.fromstring(response.content))
        )

    def search(self, term):
        response = self.session.get(
            url="{BASE_URL}/search/search.fcgi".format(BASE_URL=HTTPService.BASE_URL),
            params={"search": term},
            timeout=HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS,
        )

        response.raise_for_status()

        player_results = []

        if response.url.startswith(
            "{BASE_URL}/search/search.fcgi".format(BASE_URL=HTTPService.BASE_URL)
        ):
            page = SearchPage(html=html.fromstring(response.content))
            parsed_results = self.parser.parse_player_search_results(
                nba_aba_baa_players=page.nba_aba_baa_players
            )
            player_results += parsed_results["players"]

            seen_pagination_urls = set()
            pagination_url = page.nba_aba_baa_players_pagination_url
            while (
                pagination_url is not None
                and pagination_url not in seen_pagination_urls
            ):
                seen_pagination_urls.add(pagination_url)
                response = self.session.get(
                    url=urljoin(
                        "{BASE_URL}/search/".format(BASE_URL=HTTPService.BASE_URL),
                        pagination_url,
                    ),
                    timeout=HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS,
                )

                response.raise_for_status()

                page = SearchPage(html=html.fromstring(response.content))

                parsed_results = self.parser.parse_player_search_results(
                    nba_aba_baa_players=page.nba_aba_baa_players
                )
                player_results += parsed_results["players"]

                pagination_url = page.nba_aba_baa_players_pagination_url

        elif response.url.startswith(
            "{BASE_URL}/players".format(BASE_URL=HTTPService.BASE_URL)
        ):
            page = PlayerPage(html=html.fromstring(response.content))
            data = PlayerData(
                name=page.name,
                resource_location=response.url,
                league_abbreviations=set(
                    [
                        row.league_abbreviation
                        for row in page.totals_table.rows
                        if row.league_abbreviation is not None
                    ]
                ),
            )
            player_results += [self.parser.parse_player_data(player=data)]

        return {"players": player_results}

    def contracts(
        self, parsed_contract_row_processor: Callable[[ContractRowData], Contract]
    ) -> None:
        """
        Makes an HTTP request to fetch player contract content.
        Streams through the HTML page content in chunks, passing parsed data to the specified callback.
        This approach attempts to keep memory allocation to a minimum.
        :param parsed_contract_row_processor:
        :return:
        """
        with self.session.get(
            url=f"{HTTPService.BASE_URL}/contracts/players.html",
            stream=True,
            timeout=HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS,
        ) as response:
            if not response.ok:
                raise CouldNotGetPlayerContractData(response)

            if response.encoding is None:
                response.encoding = "utf-8"

            with PlayerContractsPageParser(
                contract_data_processor=parsed_contract_row_processor
            ) as p:
                for chunk in response.iter_content(
                    chunk_size=1024, decode_unicode=True
                ):
                    try:
                        p.parse(chunk=chunk)
                    except NothingMoreToParse:
                        break
