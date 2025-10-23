import requests

from basketball_reference_web_scraper.errors import InvalidSeason, InvalidDate, InvalidPlayerAndSeason
from basketball_reference_web_scraper.http_service import HTTPService
from basketball_reference_web_scraper.output.columns import BOX_SCORE_COLUMN_NAMES, SCHEDULE_COLUMN_NAMES, \
    PLAYER_SEASON_TOTALS_COLUMN_NAMES, \
    PLAYER_ADVANCED_SEASON_TOTALS_COLUMN_NAMES, TEAM_BOX_SCORES_COLUMN_NAMES, PLAY_BY_PLAY_COLUMN_NAMES, \
    PLAYER_SEASON_BOX_SCORE_COLUMN_NAMES, SEARCH_RESULTS_COLUMN_NAMES, STANDINGS_COLUMNS_NAMES
from basketball_reference_web_scraper.output.fields import format_value, BasketballReferenceJSONEncoder
from basketball_reference_web_scraper.output.service import OutputService
from basketball_reference_web_scraper.output.writers import CSVWriter, JSONWriter, FileOptions, OutputOptions, \
    SearchCSVWriter
from basketball_reference_web_scraper.parser_service import ParserService

# Added for support
from typing import List
import requests  # docs: https://requests.readthedocs.io/en/latest/user/quickstart/
from .data import Team, TEAM_ABBREVIATIONS_TO_TEAM
from .parser_service import parse_team_roster_names_from_team_page_html

def _team_to_abbr(team: Team) -> str:
    """
    Helper: invert TEAM_ABBREVIATIONS_TO_TEAM so we can build URLs.

    """
    # Make sure abbr is valid
    for abbr, mapped in TEAM_ABBREVIATIONS_TO_TEAM.items():
        if mapped == team:
            return abbr
    raise ValueError(f"Unsupported team: {team!r}")

def team_roster(team: Team, season_end_year: int) -> List[str]:
    """
    Purpose: return the list of player names listed on a team's roster
    for the given season end year (ex: 2025 for the 2024–25 season).

    Example:
        team_roster(Team.BOSTON_CELTICS, 2025)
        returns: ["Jayson Tatum", "Jaylen Brown", ...]
    """
    abbr = _team_to_abbr(team)
    url = f"https://www.basketball-reference.com/teams/{abbr}/{season_end_year}.html"

    # Get a page and check for HTTP errors.
    # Ref: https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()  # raises HTTPError

    # Hand off to HTML parser:
    return parse_team_roster_names_from_team_page_html(resp.text)

def standings(season_end_year, output_type=None, output_file_path=None, output_write_option=None,
              json_options=None):
    try:
        http_service = HTTPService(parser=ParserService())
        values = http_service.standings(season_end_year=season_end_year)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidSeason(season_end_year=season_end_year)
        else:
            raise http_error
    options = OutputOptions.of(
        file_options=FileOptions.of(path=output_file_path, mode=output_write_option),
        output_type=output_type,
        json_options=json_options,
        csv_options={"column_names": STANDINGS_COLUMNS_NAMES}
    )
    output_service = OutputService(
        json_writer=JSONWriter(value_formatter=BasketballReferenceJSONEncoder),
        csv_writer=CSVWriter(value_formatter=format_value)
    )
    return output_service.output(data=values, options=options)


def player_box_scores(day, month, year, output_type=None, output_file_path=None, output_write_option=None,
                      json_options=None):
    try:
        http_service = HTTPService(parser=ParserService())
        values = http_service.player_box_scores(day=day, month=month, year=year)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidDate(day=day, month=month, year=year)
        else:
            raise http_error

    options = OutputOptions.of(
        file_options=FileOptions.of(path=output_file_path, mode=output_write_option),
        output_type=output_type,
        json_options=json_options,
        csv_options={"column_names": BOX_SCORE_COLUMN_NAMES}
    )
    output_service = OutputService(
        json_writer=JSONWriter(value_formatter=BasketballReferenceJSONEncoder),
        csv_writer=CSVWriter(value_formatter=format_value)
    )
    return output_service.output(data=values, options=options)


def regular_season_player_box_scores(player_identifier, season_end_year, output_type=None, output_file_path=None,
                                     output_write_option=None, json_options=None, include_inactive_games=False):
    try:
        http_service = HTTPService(parser=ParserService())
        values = http_service.regular_season_player_box_scores(
            player_identifier=player_identifier,
            season_end_year=season_end_year,
            include_inactive_games=include_inactive_games,
        )
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.internal_server_error \
                or http_error.response.status_code == requests.codes.not_found:
            raise InvalidPlayerAndSeason(player_identifier=player_identifier, season_end_year=season_end_year)
        else:
            raise http_error
    options = OutputOptions.of(
        file_options=FileOptions.of(path=output_file_path, mode=output_write_option),
        output_type=output_type,
        json_options=json_options,
        csv_options={"column_names": PLAYER_SEASON_BOX_SCORE_COLUMN_NAMES}
    )
    output_service = OutputService(
        json_writer=JSONWriter(value_formatter=BasketballReferenceJSONEncoder),
        csv_writer=CSVWriter(value_formatter=format_value)
    )
    return output_service.output(data=values, options=options)


def playoff_player_box_scores(player_identifier, season_end_year, output_type=None, output_file_path=None,
                              output_write_option=None, json_options=None, include_inactive_games=False):
    try:
        http_service = HTTPService(parser=ParserService())
        values = http_service.playoff_player_box_scores(
            player_identifier=player_identifier,
            season_end_year=season_end_year,
            include_inactive_games=include_inactive_games,
        )
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.internal_server_error \
                or http_error.response.status_code == requests.codes.not_found:
            raise InvalidPlayerAndSeason(player_identifier=player_identifier, season_end_year=season_end_year)
        else:
            raise http_error

    options = OutputOptions.of(
        file_options=FileOptions.of(path=output_file_path, mode=output_write_option),
        output_type=output_type,
        json_options=json_options,
        csv_options={"column_names": PLAYER_SEASON_BOX_SCORE_COLUMN_NAMES}
    )
    output_service = OutputService(
        json_writer=JSONWriter(value_formatter=BasketballReferenceJSONEncoder),
        csv_writer=CSVWriter(value_formatter=format_value)
    )
    return output_service.output(data=values, options=options)


def season_schedule(season_end_year, output_type=None, output_file_path=None, output_write_option=None,
                    json_options=None):
    try:
        http_service = HTTPService(parser=ParserService())
        values = http_service.season_schedule(season_end_year=season_end_year)
    except requests.exceptions.HTTPError as http_error:
        # https://github.com/requests/requests/blob/master/requests/status_codes.py#L58
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidSeason(season_end_year=season_end_year)
        else:
            raise http_error
    options = OutputOptions.of(
        file_options=FileOptions.of(path=output_file_path, mode=output_write_option),
        output_type=output_type,
        json_options=json_options,
        csv_options={"column_names": SCHEDULE_COLUMN_NAMES}
    )
    output_service = OutputService(
        json_writer=JSONWriter(value_formatter=BasketballReferenceJSONEncoder),
        csv_writer=CSVWriter(value_formatter=format_value)
    )
    return output_service.output(data=values, options=options)


def players_season_totals(season_end_year, output_type=None, output_file_path=None, output_write_option=None,
                          json_options=None):
    try:
        http_service = HTTPService(parser=ParserService())
        values = http_service.players_season_totals(season_end_year=season_end_year)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidSeason(season_end_year=season_end_year)
        else:
            raise http_error
    options = OutputOptions.of(
        file_options=FileOptions.of(path=output_file_path, mode=output_write_option),
        output_type=output_type,
        json_options=json_options,
        csv_options={"column_names": PLAYER_SEASON_TOTALS_COLUMN_NAMES}
    )
    output_service = OutputService(
        json_writer=JSONWriter(value_formatter=BasketballReferenceJSONEncoder),
        csv_writer=CSVWriter(value_formatter=format_value)
    )
    return output_service.output(data=values, options=options)


def players_advanced_season_totals(season_end_year, include_combined_values=False, output_type=None,
                                   output_file_path=None, output_write_option=None, json_options=None):
    try:
        http_service = HTTPService(parser=ParserService())
        values = http_service.players_advanced_season_totals(
            season_end_year,
            include_combined_values=include_combined_values
        )
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidSeason(season_end_year=season_end_year)
        else:
            raise http_error
    options = OutputOptions.of(
        file_options=FileOptions.of(path=output_file_path, mode=output_write_option),
        output_type=output_type,
        json_options=json_options,
        csv_options={"column_names": PLAYER_ADVANCED_SEASON_TOTALS_COLUMN_NAMES}
    )
    output_service = OutputService(
        json_writer=JSONWriter(value_formatter=BasketballReferenceJSONEncoder),
        csv_writer=CSVWriter(value_formatter=format_value)
    )
    return output_service.output(data=values, options=options)


def team_box_scores(day, month, year, output_type=None, output_file_path=None, output_write_option=None,
                    json_options=None):
    try:
        http_service = HTTPService(parser=ParserService())
        values = http_service.team_box_scores(day=day, month=month, year=year)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidDate(day=day, month=month, year=year)
        else:
            raise http_error
    options = OutputOptions.of(
        file_options=FileOptions.of(path=output_file_path, mode=output_write_option),
        output_type=output_type,
        json_options=json_options,
        csv_options={"column_names": TEAM_BOX_SCORES_COLUMN_NAMES}
    )
    output_service = OutputService(
        json_writer=JSONWriter(value_formatter=BasketballReferenceJSONEncoder),
        csv_writer=CSVWriter(value_formatter=format_value)
    )
    return output_service.output(data=values, options=options)


def play_by_play(home_team, day, month, year, output_type=None, output_file_path=None, output_write_option=None,
                 json_options=None):
    try:
        http_service = HTTPService(parser=ParserService())
        values = http_service.play_by_play(home_team=home_team, day=day, month=month, year=year)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidDate(day=day, month=month, year=year)
        else:
            raise http_error
    options = OutputOptions.of(
        file_options=FileOptions.of(path=output_file_path, mode=output_write_option),
        output_type=output_type,
        json_options=json_options,
        csv_options={"column_names": PLAY_BY_PLAY_COLUMN_NAMES}
    )
    output_service = OutputService(
        json_writer=JSONWriter(value_formatter=BasketballReferenceJSONEncoder),
        csv_writer=CSVWriter(value_formatter=format_value)
    )
    return output_service.output(data=values, options=options)


def search(term, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    http_service = HTTPService(parser=ParserService())
    values = http_service.search(term=term)
    options = OutputOptions.of(
        file_options=FileOptions.of(path=output_file_path, mode=output_write_option),
        output_type=output_type,
        json_options=json_options,
        csv_options={"column_names": SEARCH_RESULTS_COLUMN_NAMES}
    )
    output_service = OutputService(
        json_writer=JSONWriter(value_formatter=BasketballReferenceJSONEncoder),
        csv_writer=SearchCSVWriter(value_formatter=format_value)
    )
    return output_service.output(data=values, options=options)
