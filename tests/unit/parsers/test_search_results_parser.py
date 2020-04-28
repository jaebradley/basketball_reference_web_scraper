from unittest import TestCase
from unittest.mock import MagicMock

from basketball_reference_web_scraper.data import LEAGUE_ABBREVIATIONS_TO_LEAGUE, League
from basketball_reference_web_scraper.parser_service import ParserService
from basketball_reference_web_scraper.parsers import SearchResultsParser, SearchResultNameParser, \
    ResourceLocationParser, LeagueAbbreviationParser


class TestSearchResultsParser(TestCase):
    def setUp(self):
        self.parser = SearchResultsParser(
            search_result_name_parser=SearchResultNameParser(),
            search_result_location_parser=ResourceLocationParser(
                resource_location_regex=ParserService.SEARCH_RESULT_RESOURCE_LOCATION_REGEX,
            ),
            league_abbreviation_parser=LeagueAbbreviationParser(
                abbreviations_to_league=LEAGUE_ABBREVIATIONS_TO_LEAGUE,
            ),
        )

    def test_parse_single_nba_player(self):
        players = [
            MagicMock(
                resource_name="jaebaebae",
                resource_location="https://www.basketball-reference.com/players/j/jaebaebae.html",
                league_abbreviations="NBA"
            )
        ]
        self.assertEqual(
            self.parser.parse(nba_aba_baa_players=players),
            {
                "players": [
                    {
                        "name": "jaebaebae",
                        "identifier": "jaebaebae",
                        "leagues": {League.NATIONAL_BASKETBALL_ASSOCIATION},
                    }
                ]
            }
        )

    def test_parse_single_aba_player(self):
        players = [
            MagicMock(
                resource_name="jaebaebae",
                resource_location="https://www.basketball-reference.com/players/j/jaebaebae.html",
                league_abbreviations="ABA"
            )
        ]
        self.assertEqual(
            self.parser.parse(nba_aba_baa_players=players),
            {
                "players": [
                    {
                        "name": "jaebaebae",
                        "identifier": "jaebaebae",
                        "leagues": {League.AMERICAN_BASKETBALL_ASSOCIATION},
                    }
                ]
            }
        )

    def test_parse_single_baa_player(self):
        players = [
            MagicMock(
                resource_name="jaebaebae",
                resource_location="https://www.basketball-reference.com/players/j/jaebaebae.html",
                league_abbreviations="BAA"
            )
        ]
        self.assertEqual(
            self.parser.parse(nba_aba_baa_players=players),
            {
                "players": [
                    {
                        "name": "jaebaebae",
                        "identifier": "jaebaebae",
                        "leagues": {League.BASKETBALL_ASSOCIATION_OF_AMERICA},
                    }
                ]
            }
        )

    def test_parse_single_nba_aba_baa_player(self):
        players = [
            MagicMock(
                resource_name="jaebaebae",
                resource_location="https://www.basketball-reference.com/players/j/jaebaebae.html",
                league_abbreviations="NBA/ABA/BAA"
            )
        ]
        self.assertEqual(
            self.parser.parse(nba_aba_baa_players=players),
            {
                "players": [
                    {
                        "name": "jaebaebae",
                        "identifier": "jaebaebae",
                        "leagues": {
                            League.NATIONAL_BASKETBALL_ASSOCIATION,
                            League.AMERICAN_BASKETBALL_ASSOCIATION,
                            League.BASKETBALL_ASSOCIATION_OF_AMERICA
                        },
                    }
                ]
            }
        )

    def test_parse_multiple_nba_aba_baa_players(self):
        players = [
            MagicMock(
                resource_name="jaebaebae1",
                resource_location="https://www.basketball-reference.com/players/j/jaebaebae1.html",
                league_abbreviations="NBA/ABA/BAA"
            ),
            MagicMock(
                resource_name="jaebaebae2",
                resource_location="https://www.basketball-reference.com/players/j/jaebaebae2.html",
                league_abbreviations="NBA/ABA/BAA"
            ),
            MagicMock(
                resource_name="jaebaebae3",
                resource_location="https://www.basketball-reference.com/players/j/jaebaebae3.html",
                league_abbreviations="NBA/ABA/BAA"
            )
        ]
        self.assertEqual(
            self.parser.parse(nba_aba_baa_players=players),
            {
                "players": [
                    {
                        "name": "jaebaebae1",
                        "identifier": "jaebaebae1",
                        "leagues": {
                            League.NATIONAL_BASKETBALL_ASSOCIATION,
                            League.AMERICAN_BASKETBALL_ASSOCIATION,
                            League.BASKETBALL_ASSOCIATION_OF_AMERICA,
                        },
                    },
                    {
                        "name": "jaebaebae2",
                        "identifier": "jaebaebae2",
                        "leagues": {
                            League.NATIONAL_BASKETBALL_ASSOCIATION,
                            League.AMERICAN_BASKETBALL_ASSOCIATION,
                            League.BASKETBALL_ASSOCIATION_OF_AMERICA,
                        },
                    },
                    {
                        "name": "jaebaebae3",
                        "identifier": "jaebaebae3",
                        "leagues": {
                            League.NATIONAL_BASKETBALL_ASSOCIATION,
                            League.AMERICAN_BASKETBALL_ASSOCIATION,
                            League.BASKETBALL_ASSOCIATION_OF_AMERICA,
                        },
                    },
                ]
            }
        )
