import csv
import json

from basketball_reference_web_scraper.data import OutputWriteOption
from basketball_reference_web_scraper.utilities import merge_two_dicts


class WriteOptions:
    def __init__(self, data, file_path, mode, custom_options):
        self.data = data
        self.file_path = file_path
        self.mode = mode
        self.custom_options = custom_options

    def should_write_to_file(self):
        return self.file_path is not None and self.mode is not None


class JSONWriter:
    DEFAULT_OPTIONS = {
        "sort_keys": True,
        "indent": 4,
    }

    def __init__(self, encoder):
        self.encoder = encoder

    def write(self, data, options):
        output_options = self.DEFAULT_OPTIONS if options.custom_options is None else merge_two_dicts(
            first=self.DEFAULT_OPTIONS,
            second=options.custom_options
        )

        if options.should_write_to_file:
            with open(options.file_path, options.mode.value, newline="") as json_file:
                return json.dump(data, json_file, cls=self.encoder, **output_options)

        return json.dumps(data, cls=self.encoder, **output_options)


class CSVWriter:
    def __init__(self, column_names, row_formatter):
        self.column_names = column_names
        self.row_formatter = row_formatter

    def write(self, data, options):
        if options.should_write_to_file:
            with open(options.file_path, options.mode.value, newline="") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.column_names)
                writer.writeheader()
                writer.writerows(self.row_formatter.format(row_data) for row_data in data)

        raise ValueError("CSV output must contain a file path")


class RowFormatter:
    def __init__(self, data_field_names):
        self.data_field_names = data_field_names

    def format(self, row_data):
        return {
            field_name: row_data[field_name]
            for field_name in self.data_field_names
        }


class BoxScoreRowFormatter(RowFormatter):
    def __init__(self):
        RowFormatter.__init__(
            self,
            data_field_names=[
                "team",
                "minutes_played",
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
            ]
        )

    def format(self, row_data):
        return {
            data_field_name: row_data[data_field_name].value
            if data_field_name in ["team", "location", "opponent", "outcome"]
            else row_data[data_field_name]
            for data_field_name in self.data_field_names
        }


class ScheduleRowFormatter(RowFormatter):
    def __init__(self):
        RowFormatter.__init__(
            self,
            data_field_names=[
                "start_time",
                "away_team",
                "home_team",
                "away_team_score",
                "home_team_score",
            ]
        )

    def format(self, row_data):
        return {
            data_field_name: row_data[data_field_name].value
            if data_field_name in ["away_team", "home_team"]
            else row_data[data_field_name]
            for data_field_name in self.data_field_names
        }


class PlayerSeasonTotalsRowFormatter(RowFormatter):
    def __init__(self):
        RowFormatter.__init__(
            self,
            data_field_names=[
                "slug",
                "name",
                "positions",
                "age",
                "team",
                "games_played",
                "games_started",
                "minutes_played",
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
            ]
        )

    def format(self, row_data):
        return {
            data_field_name: "-".join(map(lambda position: position.value, row_data[data_field_name]))
            if data_field_name == "positions"
            else row_data[data_field_name].value if data_field_name == "team"
            else row_data[data_field_name]
            for data_field_name in self.data_field_names
        }


class TeamBoxScoreRowFormatter(RowFormatter):
    def __init__(self):
        RowFormatter.__init__(
            self,
            data_field_names=[
                "team",
                "minutes_played",
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
            ]
        )

    def format(self, row_data):
        return {
            data_field_name: row_data[data_field_name].value
            if data_field_name == "team"
            else row_data[data_field_name]
            for data_field_name in self.data_field_names
        }


class BoxScoreCSVWriter(CSVWriter):
    def __init__(self, option=OutputWriteOption.CREATE_AND_WRITE):
        CSVWriter.__init__(
            self,
            column_names=[
                "slug",
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
            ],
            row_formatter=BoxScoreRowFormatter(),
            option=option,
        )


class ScheduleCSVWriter(CSVWriter):
    def __init__(self, option=OutputWriteOption.CREATE_AND_WRITE):
        CSVWriter.__init__(
            self,
            column_names=[
                "team",
                "minutes_played",
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
            ],
            row_formatter=ScheduleRowFormatter(),
            option=option
        )
