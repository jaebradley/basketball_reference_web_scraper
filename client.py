from http_client import get_box_scores, get_season_schedule

from output import box_scores_to_csv, schedule_to_csv
from output import output
from json_encoders import ScheduleEncoder


def box_scores(day, month, year, output_type=None, relative_file_path=None, json_options=None):
    values = get_box_scores(day=day, month=month, year=year)
    return output(
        values=values,
        output_type=output_type,
        relative_file_path=relative_file_path,
        csv_writer=box_scores_to_csv,
        encoder=None,
        json_options=json_options,
    )


def season_schedule(season_end_year, output_type=None, relative_file_path=None, json_options=None):
    values = get_season_schedule(season_end_year)
    return output(
        values=values,
        output_type=output_type,
        relative_file_path=relative_file_path,
        csv_writer=schedule_to_csv,
        encoder=ScheduleEncoder,
        json_options=json_options,
    )

