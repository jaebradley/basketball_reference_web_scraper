import requests
from lxml import html

from basketball_reference_web_scraper.data import LEAGUE_ABBREVIATIONS_TO_LEAGUE, PlayerData
from basketball_reference_web_scraper.html import SearchPage, PlayerPage
from basketball_reference_web_scraper.parsers import SearchResultNameParser, \
    ResourceLocationParser, SearchResultsParser, LeagueAbbreviationParser, PlayerDataParser

BASE_URL = 'https://www.basketball-reference.com'
PLAY_BY_PLAY_TIMESTAMP_FORMAT = "%M:%S.%f"
SEARCH_RESULT_RESOURCE_LOCATION_REGEX = '(https?:\/\/www\.basketball-reference\.com\/)?(?P<resource_type>.+?(?=\/)).*\/(?P<resource_identifier>.+).html'


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
