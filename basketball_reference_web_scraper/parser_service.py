from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM, LOCATION_ABBREVIATIONS_TO_POSITION, OUTCOME_ABBREVIATIONS_TO_OUTCOME, TEAM_NAME_TO_TEAM, \
    POSITION_ABBREVIATIONS_TO_POSITION, LEAGUE_ABBREVIATIONS_TO_LEAGUE, Division, Team, DIVISIONS_TO_CONFERENCES
from basketball_reference_web_scraper.parsers import PositionAbbreviationParser, TeamAbbreviationParser, \
    PlayerSeasonTotalsParser, TeamTotalsParser, LocationAbbreviationParser, OutcomeAbbreviationParser, \
    SecondsPlayedParser, PlayerBoxScoresParser, PlayerAdvancedSeasonTotalsParser, PeriodDetailsParser, \
    PeriodTimestampParser, ScoresParser, PlayByPlaysParser, TeamNameParser, ScheduledStartTimeParser, \
    ScheduledGamesParser, PlayerBoxScoreOutcomeParser, PlayerSeasonBoxScoresParser, SearchResultNameParser, \
    ResourceLocationParser, SearchResultsParser, LeagueAbbreviationParser, PlayerDataParser, DivisionNameParser, \
    TeamStandingsParser, ConferenceDivisionStandingsParser

import re
from typing import List
from bs4 import BeautifulSoup, Comment  # docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
def parse_team_roster_names_from_team_page_html(html: str) -> List[str]:
    """
    Given the raw HTML for a Basketball-Reference page
    (like https://www.basketball-reference.com/teams/BOS/2025.html),
    return a simple list of player names as they appear in the roster table.

    Steps:
      1) Parse HTML into a soup (Ref: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#quick-start)
      2) Find <table id="roster">. If not present, could be commented out,
         so scan HTML comments too.
      3) Walk the table rows in <tbody>, grab the player's name from the header cell
         <th scope="row">.
    """
    # 1) Build a DOM tree for easy calls
    soup = BeautifulSoup(html, "html.parser")

    # 2a) Normal case: roster table there
    table = soup.find("table", id="roster")

    # 2b) Commented out (they're being annoying):
    #     Scan comment nodes and parse to search again.
    #     Ref: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#comments-and-other-special-strings
    if table is None:
        for node in soup.find_all(string=lambda s: isinstance(s, Comment)):
            frag = BeautifulSoup(node, "html.parser")
            table = frag.find("table", id="roster")
            if table:
                break

    # If no usable roster table, return nothing
    if table is None or table.tbody is None:
        return []

    names: List[str] = []

    # 3) Iterate direct <tr> rows in <tbody> and get name from the row header cell.
    for row in table.tbody.find_all("tr", recursive=False):
        th = row.find("th", attrs={"scope": "row"})
        if th is None:
            continue  # skip odd rows (headers/separators)

        a = th.find("a")  # name usually inside a link
        if a and a.text:
            names.append(a.text.strip())
        else:
            # Fallback to whatever text the header cell has
            text = th.get_text(strip=True)
            if text:
                names.append(text)

    return names

class ParserService:
    PLAY_BY_PLAY_TIMESTAMP_FORMAT = "%M:%S.%f"
    PLAY_BY_PLAY_SCORES_REGEX = "(?P<away_team_score>[0-9]+)-(?P<home_team_score>[0-9]+)"
    SEARCH_RESULT_RESOURCE_LOCATION_REGEX = re.compile(r'(https?:\/\/www\.basketball-reference\.com\/)?(?P<resource_type>.+?(?=\/)).*\/(?P<resource_identifier>.+).html')

    def __init__(self):
        self.team_abbreviation_parser = TeamAbbreviationParser(abbreviations_to_teams=TEAM_ABBREVIATIONS_TO_TEAM)
        self.league_abbreviation_parser=LeagueAbbreviationParser(abbreviations_to_league=LEAGUE_ABBREVIATIONS_TO_LEAGUE)
        self.location_abbreviation_parser = LocationAbbreviationParser(
            abbreviations_to_locations=LOCATION_ABBREVIATIONS_TO_POSITION,
        )
        self.outcome_abbreviation_parser = OutcomeAbbreviationParser(
            abbreviations_to_outcomes=OUTCOME_ABBREVIATIONS_TO_OUTCOME,
        )
        self.outcome_parser = PlayerBoxScoreOutcomeParser(outcome_abbreviation_parser=self.outcome_abbreviation_parser)
        self.period_details_parser = PeriodDetailsParser(regulation_periods_count=4)
        self.period_timestamp_parser = PeriodTimestampParser(timestamp_format=ParserService.PLAY_BY_PLAY_TIMESTAMP_FORMAT)
        self.position_abbreviation_parser = PositionAbbreviationParser(
            abbreviations_to_positions=POSITION_ABBREVIATIONS_TO_POSITION,
        )
        self.seconds_played_parser = SecondsPlayedParser()
        self.scores_parser = ScoresParser(scores_regex=ParserService.PLAY_BY_PLAY_SCORES_REGEX)
        self.search_result_name_parser = SearchResultNameParser()
        self.search_result_location_parser = ResourceLocationParser(
            resource_location_regex=ParserService.SEARCH_RESULT_RESOURCE_LOCATION_REGEX
        )
        self.team_name_parser = TeamNameParser(team_names_to_teams=TEAM_NAME_TO_TEAM)

        self.play_by_plays_parser = PlayByPlaysParser(
            period_details_parser=self.period_details_parser,
            period_timestamp_parser=self.period_timestamp_parser,
            scores_parser=self.scores_parser,
        )
        self.player_box_scores_parser = PlayerBoxScoresParser(
            team_abbreviation_parser=self.team_abbreviation_parser,
            location_abbreviation_parser=self.location_abbreviation_parser,
            outcome_abbreviation_parser=self.outcome_abbreviation_parser,
            seconds_played_parser=self.seconds_played_parser
        )
        self.player_data_parser = PlayerDataParser(
            search_result_location_parser=self.search_result_location_parser,
            league_abbreviation_parser=self.league_abbreviation_parser,
        )
        self.player_season_box_scores_parser = PlayerSeasonBoxScoresParser(
            team_abbreviation_parser=self.team_abbreviation_parser,
            location_abbreviation_parser=self.location_abbreviation_parser,
            outcome_parser=self.outcome_parser,
            seconds_played_parser=self.seconds_played_parser
        )
        self.player_season_totals_parser = PlayerSeasonTotalsParser(
            position_abbreviation_parser=self.position_abbreviation_parser,
            team_abbreviation_parser=self.team_abbreviation_parser,
        )
        self.player_advanced_season_totals_parser = PlayerAdvancedSeasonTotalsParser(
            team_abbreviation_parser=self.team_abbreviation_parser,
            position_abbreviation_parser=self.position_abbreviation_parser,
        )
        self.scheduled_start_time_parser = ScheduledStartTimeParser()
        self.scheduled_games_parser = ScheduledGamesParser(
            start_time_parser=self.scheduled_start_time_parser,
            team_name_parser=self.team_name_parser,
        )
        self.search_results_parser = SearchResultsParser(
            search_result_name_parser=self.search_result_name_parser,
            search_result_location_parser=self.search_result_location_parser,
            league_abbreviation_parser=self.league_abbreviation_parser,
        )
        self.team_totals_parser = TeamTotalsParser(team_abbreviation_parser=self.team_abbreviation_parser)
        self.division_name_parser = DivisionNameParser(divisions=Division)
        self.team_standings_parser = TeamStandingsParser(teams=Team)
        self.conference_division_standings_parser = ConferenceDivisionStandingsParser(
            division_name_parser=self.division_name_parser,
            team_standings_parser=self.team_standings_parser,
            divisions_to_conferences=DIVISIONS_TO_CONFERENCES,
        )

    def parse_division_standings(self, standings):
        return self.conference_division_standings_parser.parse(division_standings=standings)

    def parse_play_by_plays(self, play_by_plays, away_team_name, home_team_name):
        return self.play_by_plays_parser.parse(
            play_by_plays=play_by_plays,
            away_team=self.team_name_parser.parse_team_name(team_name=away_team_name),
            home_team=self.team_name_parser.parse_team_name(team_name=home_team_name),
        )

    def parse_player_box_scores(self, box_scores):
        return self.player_box_scores_parser.parse(box_scores=box_scores)

    def parse_player_season_box_scores(self, box_scores, include_inactive_games=False):
        return self.player_season_box_scores_parser.parse(box_scores=box_scores, include_inactive_games=include_inactive_games)

    def parse_player_advanced_season_totals_parser(self, totals):
        return self.player_advanced_season_totals_parser.parse(totals=totals)

    def parse_player_season_totals(self, totals):
        return self.player_season_totals_parser.parse(totals=totals)

    def parse_scheduled_games(self, games):
        return self.scheduled_games_parser.parse_games(games)

    def parse_team_totals(self, first_team_totals, second_team_totals):
        return self.team_totals_parser.parse(first_team_totals=first_team_totals, second_team_totals=second_team_totals)

    def parse_player_search_results(self, nba_aba_baa_players):
        return self.search_results_parser.parse(nba_aba_baa_players=nba_aba_baa_players)

    def parse_player_data(self, player):
        return self.player_data_parser.parse(player=player)