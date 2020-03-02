import requests
from lxml import html

from basketball_reference_web_scraper.data import TEAM_TO_TEAM_ABBREVIATION, TEAM_ABBREVIATIONS_TO_TEAM, TeamTotal, \
    LOCATION_ABBREVIATIONS_TO_POSITION, OUTCOME_ABBREVIATIONS_TO_OUTCOME, TEAM_NAME_TO_TEAM, \
    POSITION_ABBREVIATIONS_TO_POSITION, LEAGUE_ABBREVIATIONS_TO_LEAGUE, PlayerData
from basketball_reference_web_scraper.errors import InvalidDate, InvalidPlayerAndSeason
from basketball_reference_web_scraper.html import PlayerSeasonTotalTable, BoxScoresPage, DailyLeadersPage, \
    PlayerAdvancedSeasonTotalsTable, PlayByPlayPage, DailyBoxScoresPage, SchedulePage, PlayerSeasonBoxScoresPage, \
    SearchPage, PlayerPage
from basketball_reference_web_scraper.parsers import PositionAbbreviationParser, TeamAbbreviationParser, \
    PlayerSeasonTotalsParser, TeamTotalsParser, LocationAbbreviationParser, OutcomeAbbreviationParser, \
    SecondsPlayedParser, PlayerBoxScoresParser, PlayerAdvancedSeasonTotalsParser, PeriodDetailsParser, \
    PeriodTimestampParser, ScoresParser, PlayByPlaysParser, TeamNameParser, ScheduledStartTimeParser, \
    ScheduledGamesParser, PlayerBoxScoreOutcomeParser, PlayerSeasonBoxScoresParser, SearchResultNameParser, \
    ResourceLocationParser, SearchResultsParser, LeagueAbbreviationParser, PlayerDataParser

BASE_URL = 'https://www.basketball-reference.com'
PLAY_BY_PLAY_TIMESTAMP_FORMAT = "%M:%S.%f"
PLAY_BY_PLAY_SCORES_REGEX = "(?P<away_team_score>[0-9]+)-(?P<home_team_score>[0-9]+)"
SEARCH_RESULT_RESOURCE_LOCATION_REGEX = '(https?:\/\/www\.basketball-reference\.com\/)?(?P<resource_type>.+?(?=\/)).*\/(?P<resource_identifier>.+).html'


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
        page = DailyLeadersPage(html=html.fromstring(response.content))
        box_score_parser = PlayerBoxScoresParser(
            team_abbreviation_parser=TeamAbbreviationParser(
                abbreviations_to_teams=TEAM_ABBREVIATIONS_TO_TEAM
            ),
            location_abbreviation_parser=LocationAbbreviationParser(
                abbreviations_to_locations=LOCATION_ABBREVIATIONS_TO_POSITION
            ),
            outcome_abbreviation_parser=OutcomeAbbreviationParser(
                abbreviations_to_outcomes=OUTCOME_ABBREVIATIONS_TO_OUTCOME
            ),
            seconds_played_parser=SecondsPlayedParser(),
        )
        return box_score_parser.parse(page.daily_leaders)

    raise InvalidDate(day=day, month=month, year=year)


def regular_season_player_box_scores(player_identifier, season_end_year):
    # Makes assumption that basketball reference pattern of breaking out player pathing using first character of
    # surname can be derived from the fact that basketball reference also has a pattern of player identifiers
    # starting with first few characters of player's surname
    url = '{BASE_URL}/players/{player_surname_starting_character}/{player_identifier}/gamelog/{season_end_year}'.format(
        BASE_URL=BASE_URL,
        player_surname_starting_character=player_identifier[0],
        player_identifier=player_identifier,
        season_end_year=season_end_year,
    )

    response = requests.get(url=url, allow_redirects=False)
    response.raise_for_status()

    page = PlayerSeasonBoxScoresPage(html=html.fromstring(response.content))
    if page.regular_season_box_scores_table is None:
        raise InvalidPlayerAndSeason(player_identifier=player_identifier, season_end_year=season_end_year)

    parser = PlayerSeasonBoxScoresParser(
        team_abbreviation_parser=TeamAbbreviationParser(
            abbreviations_to_teams=TEAM_ABBREVIATIONS_TO_TEAM
        ),
        location_abbreviation_parser=LocationAbbreviationParser(
            abbreviations_to_locations=LOCATION_ABBREVIATIONS_TO_POSITION
        ),
        outcome_parser=PlayerBoxScoreOutcomeParser(
            outcome_abbreviation_parser=OutcomeAbbreviationParser(
                abbreviations_to_outcomes=OUTCOME_ABBREVIATIONS_TO_OUTCOME
            ),
        ),
        seconds_played_parser=SecondsPlayedParser(),
    )
    return parser.parse(box_scores=page.regular_season_box_scores_table.rows)


def schedule_for_month(url):
    response = requests.get(url=url)

    response.raise_for_status()

    page = SchedulePage(html=html.fromstring(html=response.content))
    parser = ScheduledGamesParser(
        start_time_parser=ScheduledStartTimeParser(),
        team_name_parser=TeamNameParser(team_names_to_teams=TEAM_NAME_TO_TEAM),
    )
    return parser.parse_games(games=page.rows)


def season_schedule(season_end_year):
    url = '{BASE_URL}/leagues/NBA_{season_end_year}_games.html'.format(
        BASE_URL=BASE_URL,
        season_end_year=season_end_year
    )

    response = requests.get(url=url)

    response.raise_for_status()

    page = SchedulePage(html=html.fromstring(html=response.content))
    parser = ScheduledGamesParser(
        start_time_parser=ScheduledStartTimeParser(),
        team_name_parser=TeamNameParser(team_names_to_teams=TEAM_NAME_TO_TEAM),
    )
    season_schedule_values = parser.parse_games(games=page.rows)

    for month_url_path in page.other_months_schedule_urls:
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


def players_advanced_season_totals(season_end_year, include_combined_values=False):
    url = '{BASE_URL}/leagues/NBA_{season_end_year}_advanced.html'.format(
        BASE_URL=BASE_URL,
        season_end_year=season_end_year,
    )

    response = requests.get(url=url)

    response.raise_for_status()

    table = PlayerAdvancedSeasonTotalsTable(html=html.fromstring(response.content))
    parser = PlayerAdvancedSeasonTotalsParser(
        team_abbreviation_parser=TeamAbbreviationParser(
            abbreviations_to_teams=TEAM_ABBREVIATIONS_TO_TEAM
        ),
        position_abbreviation_parser=PositionAbbreviationParser(
            abbreviations_to_positions=POSITION_ABBREVIATIONS_TO_POSITION
        )
    )

    return parser.parse(table.get_rows(include_combined_values))


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

    return parser.parse(
        first_team_totals=combined_team_totals[0],
        second_team_totals=combined_team_totals[1],
    )


def team_box_scores(day, month, year):
    url = "{BASE_URL}/boxscores/".format(BASE_URL=BASE_URL)

    response = requests.get(url=url, params={"day": day, "month": month, "year": year})

    response.raise_for_status()

    page = DailyBoxScoresPage(html=html.fromstring(response.content))

    return [
        box_score
        for game_url_path in page.game_url_paths
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
    page = PlayByPlayPage(html=html.fromstring(response.content))

    play_by_plays_parser = PlayByPlaysParser(
        period_details_parser=PeriodDetailsParser(regulation_periods_count=4),
        period_timestamp_parser=PeriodTimestampParser(timestamp_format=PLAY_BY_PLAY_TIMESTAMP_FORMAT),
        scores_parser=ScoresParser(scores_regex=PLAY_BY_PLAY_SCORES_REGEX))

    team_name_parser = TeamNameParser(team_names_to_teams=TEAM_NAME_TO_TEAM)

    return play_by_plays_parser.parse(play_by_plays=page.play_by_play_table.rows,
                                      away_team=team_name_parser.parse_team_name(team_name=page.away_team_name),
                                      home_team=team_name_parser.parse_team_name(team_name=page.home_team_name))


def search(term):
    response = requests.get(
        url="{BASE_URL}/search/search.fcgi".format(BASE_URL=BASE_URL),
        params={"search": term}
    )

    response.raise_for_status()

    player_results = []

    if response.url.startswith("{BASE_URL}/search/search.fcgi".format(BASE_URL=BASE_URL)):
        page = SearchPage(html=html.fromstring(response.content))

        parser = SearchResultsParser(
            search_result_name_parser=SearchResultNameParser(),
            search_result_location_parser=ResourceLocationParser(
                resource_location_regex=SEARCH_RESULT_RESOURCE_LOCATION_REGEX,
            ),
            league_abbreviation_parser=LeagueAbbreviationParser(
                abbreviations_to_league=LEAGUE_ABBREVIATIONS_TO_LEAGUE,
            ),
        )

        parsed_results = parser.parse(nba_aba_baa_players=page.nba_aba_baa_players)
        player_results += parsed_results["players"]

        while page.nba_aba_baa_players_pagination_url is not None:
            response = requests.get(
                url="{BASE_URL}/search/{pagination_url}".format(
                    BASE_URL=BASE_URL,
                    pagination_url=page.nba_aba_baa_players_pagination_url
                )
            )

            response.raise_for_status()

            page = SearchPage(html=html.fromstring(response.content))

            parsed_results = parser.parse(nba_aba_baa_players=page.nba_aba_baa_players)
            player_results += parsed_results["players"]

    elif response.url.startswith("{BASE_URL}/players".format(BASE_URL=BASE_URL)):
        page = PlayerPage(html=html.fromstring(response.content))
        data = PlayerData(
            name=page.name,
            resource_location=response.url,
            league_abbreviations=set([row.league_abbreviation for row in page.totals_table.rows])
        )
        parser = PlayerDataParser(
            search_result_location_parser=ResourceLocationParser(
                resource_location_regex=SEARCH_RESULT_RESOURCE_LOCATION_REGEX,
            ),
            league_abbreviation_parser=LeagueAbbreviationParser(abbreviations_to_league=LEAGUE_ABBREVIATIONS_TO_LEAGUE),
        )
        player_results += [parser.parse(player=data)]

    return {
        "players": player_results
    }
