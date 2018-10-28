import http_client

from output import box_scores_to_csv, schedule_to_csv
from output import output
from json_encoders import BasketballReferenceJSONEncoder


def box_scores(day, month, year, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    values = http_client.box_scores(day=day, month=month, year=year)
    return output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=box_scores_to_csv,
        encoder=BasketballReferenceJSONEncoder,
        json_options=json_options,
    )


def season_schedule(season_end_year, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    values = http_client.season_schedule(season_end_year)
    return output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=schedule_to_csv,
        encoder=BasketballReferenceJSONEncoder,
        json_options=json_options,
    )

