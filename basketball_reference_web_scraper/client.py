from typing import Any, Callable

import requests
from basketball_reference_web_scraper.contracts.data.models import Contract, Player
from basketball_reference_web_scraper.contracts.data.parsers import ContractsTableRowParser, \
    SalariesBySeasonParser, deserialize_season_start_year, deserialize_guaranteed_salary, \
    deserialize_optional_salary, deserialize_team
from basketball_reference_web_scraper.errors import InvalidSeason, InvalidDate, InvalidPlayerAndSeason, \
    InvalidTeamSeason
from basketball_reference_web_scraper.http_service import HTTPService
from basketball_reference_web_scraper.output.columns import BOX_SCORE_COLUMN_NAMES, SCHEDULE_COLUMN_NAMES, \
    PLAYER_SEASON_TOTALS_COLUMN_NAMES, \
    PLAYER_ADVANCED_SEASON_TOTALS_COLUMN_NAMES, TEAM_BOX_SCORES_COLUMN_NAMES, PLAY_BY_PLAY_COLUMN_NAMES, \
    PLAYER_SEASON_BOX_SCORE_COLUMN_NAMES, SEARCH_RESULTS_COLUMN_NAMES, STANDINGS_COLUMNS_NAMES, ROSTER_COLUMN_NAMES
from basketball_reference_web_scraper.output.fields import format_value, BasketballReferenceJSONEncoder
from basketball_reference_web_scraper.output.service import OutputService
from basketball_reference_web_scraper.output.writers import CSVWriter, JSONWriter, FileOptions, OutputOptions, \
    SearchCSVWriter
from basketball_reference_web_scraper.parser_service import ParserService

__contracts_table_row_parser = ContractsTableRowParser(
    salary_generator=SalariesBySeasonParser(season_start_year_deserializer=deserialize_season_start_year,
                                            salary_deserializer=deserialize_optional_salary),
    guaranteed_salary_generator=deserialize_guaranteed_salary,
    player_generator=lambda row: Player(identifier=row.id, name=row.name),
    team_generator=deserialize_team,
)


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


def players_regular_season_shooting_statistics(season_end_year):
    try:
        http_service = HTTPService(parser=ParserService())
        values = http_service.players_season_shooting_statistics(season_end_year=season_end_year)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidSeason(season_end_year=season_end_year)
        else:
            raise http_error

    return values


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


def roster(team, season_end_year, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    try:
        http_service = HTTPService(parser=ParserService())
        values = http_service.roster(team=team, season_end_year=season_end_year)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidTeamSeason(team=team, year=season_end_year)
        else:
            raise http_error

    options = OutputOptions.of(
        file_options=FileOptions.of(path=output_file_path, mode=output_write_option),
        output_type=output_type,
        json_options=json_options,
        csv_options={"column_names": ROSTER_COLUMN_NAMES}
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


def contracts(contract_processor: Callable[[Contract], Any]):
    """
    Parses player contract data found on this page: https://www.basketball-reference.com/contracts/players.html
    PlayerContract results are processed by the client caller via a callback.

    For example:
    client.player_contracts(player_contract_processor=lambda player_contract_data: print(player_contract_data))

    :param contract_processor:
    :return: None
    :raises: CouldNotGetPlayerContractData
    """
    HTTPService(parser=ParserService()).contracts(
        parsed_contract_row_processor=lambda contract_data: contract_processor(
            __contracts_table_row_parser.parse_combined_row_data(data=contract_data)))
