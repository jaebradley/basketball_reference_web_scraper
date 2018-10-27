import csv
import json

from data import OutputType
from errors import UnknownOutputType

box_score_fieldname = [
    "name",
    "team",
    "location",
    "opponent",
    "outcome",
    "seconds_played",
    "made_field_goals",
    "attempted_field_goals",
    "made_three_point_field_goals",
    "attempted_three_point_field_goals",
    "made_free_throws",
    "attempted_free_throws",
    "offensive_rebounds",
    "defensive_rebounds",
    "assists",
    "steals",
    "blocks",
    "turnovers",
    "personal_fouls",
    "game_score",
]

game_fieldname = [
    "start_time",
    "away_team",
    "away_team_score",
    "home_team",
    "home_team_score",
]

default_json_options = {
    "sort_keys": True,
    "indent": 4,
}


def output(values, output_type, relative_file_path, encoder, csv_writer, json_options=None):
    if output_type is None:
        return values

    if output_type == OutputType.JSON:
        options = default_json_options if json_options is None else {**default_json_options, **json_options}
        return json.dumps(values, cls=encoder, **options)

    if output_type == OutputType.CSV:
        if relative_file_path is None:
            raise ValueError("CSV output must contain a file path")
        else:
            return csv_writer(rows=values, relative_file_path=relative_file_path)

    raise UnknownOutputType(output_type)


def box_scores_to_csv(rows, relative_file_path):
    write_csv(rows=rows, fieldnames=box_score_fieldname, relative_file_path=relative_file_path)


def schedule_to_csv(rows, relative_file_path):
    write_csv(rows=rows, fieldnames=game_fieldname, relative_file_path=relative_file_path)


def write_csv(rows, fieldnames, relative_file_path):
    with open(relative_file_path, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
