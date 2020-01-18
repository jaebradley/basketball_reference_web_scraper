import requests

from basketball_reference_web_scraper import http_client
from basketball_reference_web_scraper.errors import InvalidSeason, InvalidDate, InvalidPlayer
from basketball_reference_web_scraper.output import output
from basketball_reference_web_scraper.writers import CSVWriter, RowFormatter, \
    BOX_SCORE_COLUMN_NAMES, SCHEDULE_COLUMN_NAMES, PLAYER_SEASON_TOTALS_COLUMN_NAMES, \
    PLAYER_ADVANCED_SEASON_TOTALS_COLUMN_NAMES, TEAM_BOX_SCORES_COLUMN_NAMES, PLAY_BY_PLAY_COLUMN_NAMES


def player_box_scores(day, month, year, output_type=None, output_file_path=None, output_write_option=None,
                      json_options=None):
    try:
        values = http_client.player_box_scores(day=day, month=month, year=year)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidDate(day=day, month=month, year=year)
        else:
            raise http_error
    return output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=CSVWriter(
            column_names=BOX_SCORE_COLUMN_NAMES,
            row_formatter=RowFormatter(data_field_names=BOX_SCORE_COLUMN_NAMES)
        ),
        json_options=json_options,
    )


def player_season_box_scores(player_name, season_end_year, url_override='01', output_type=None, output_file_path=None, output_write_option=None,
                             json_options=None):

    # TODO (url_override hax):
    # the bballref url link for a player's season box score contains:
    #    <first 5 letters of last name><first 2 letters of first name><duplication id>
    # the duplication id defaults to 01, but if there are two or more players that
    # have similar names (e.g. Jabari Brown and Jaylen Brown are both brownja),
    # then the duplication id is what sets them apart (i.e. brownja01 & brownja02).
    # allow the user to manually pass this in for now until we can find a better
    # method of resolving the correct id.
    try:
        values = http_client.player_season_box_scores(player_name, season_end_year, url_override)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.internal_server_error:
            raise InvalidPlayer(player_name)
        else:
            raise http_error
    return output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=CSVWriter(
            column_names=BOX_SCORE_COLUMN_NAMES,
            row_formatter=RowFormatter(data_field_names=BOX_SCORE_COLUMN_NAMES)
        ),
        json_options=json_options,
    )


def season_schedule(season_end_year, output_type=None, output_file_path=None, output_write_option=None,
                    json_options=None):
    try:
        values = http_client.season_schedule(season_end_year)
    except requests.exceptions.HTTPError as http_error:
        # https://github.com/requests/requests/blob/master/requests/status_codes.py#L58
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidSeason(season_end_year=season_end_year)
        else:
            raise http_error
    return output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=CSVWriter(
            column_names=SCHEDULE_COLUMN_NAMES,
            row_formatter=RowFormatter(data_field_names=SCHEDULE_COLUMN_NAMES)
        ),
        json_options=json_options,
    )


def players_season_totals(season_end_year, output_type=None, output_file_path=None, output_write_option=None,
                          json_options=None):
    try:
        values = http_client.players_season_totals(season_end_year)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidSeason(season_end_year=season_end_year)
        else:
            raise http_error
    return output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=CSVWriter(
            column_names=PLAYER_SEASON_TOTALS_COLUMN_NAMES,
            row_formatter=RowFormatter(data_field_names=PLAYER_SEASON_TOTALS_COLUMN_NAMES)
        ),
        json_options=json_options,
    )


def players_advanced_season_totals(season_end_year, output_type=None, output_file_path=None, output_write_option=None,
                                   json_options=None):
    try:
        values = http_client.players_advanced_season_totals(season_end_year)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidSeason(season_end_year=season_end_year)
        else:
            raise http_error
    return output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=CSVWriter(
            column_names=PLAYER_ADVANCED_SEASON_TOTALS_COLUMN_NAMES,
            row_formatter=RowFormatter(data_field_names=PLAYER_ADVANCED_SEASON_TOTALS_COLUMN_NAMES)
        ),
        json_options=json_options,
    )


def team_box_scores(day, month, year, output_type=None, output_file_path=None, output_write_option=None,
                    json_options=None):
    try:
        values = http_client.team_box_scores(day=day, month=month, year=year)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidDate(day=day, month=month, year=year)
        else:
            raise http_error
    return output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=CSVWriter(
            column_names=TEAM_BOX_SCORES_COLUMN_NAMES,
            row_formatter=RowFormatter(data_field_names=TEAM_BOX_SCORES_COLUMN_NAMES)
        ),
        json_options=json_options,
    )


def play_by_play(home_team, day, month, year, output_type=None, output_file_path=None, output_write_option=None,
                 json_options=None):
    try:
        values = http_client.play_by_play(home_team=home_team, day=day, month=month, year=year)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidDate(day=day, month=month, year=year)
        else:
            raise http_error
    return output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=CSVWriter(
            column_names=PLAY_BY_PLAY_COLUMN_NAMES,
            row_formatter=RowFormatter(data_field_names=PLAY_BY_PLAY_COLUMN_NAMES)
        ),
        json_options=json_options,
    )
