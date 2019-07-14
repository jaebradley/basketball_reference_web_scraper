import csv
import json

from basketball_reference_web_scraper.data import OutputWriteOption
from basketball_reference_web_scraper.utilities import merge_two_dicts

# I wrote the explicit mapping of CSV values because there didn't seem to be a way of outputting the values of enums
# without doing it this way


BOX_SCORE_COLUMN_NAMES = [
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
]

SCHEDULE_COLUMN_NAMES = [
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

PLAYER_SEASON_TOTALS_COLUMN_NAMES = [
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

PLAYER_ADVANCED_SEASON_TOTALS_COLUMN_NAMES = [
    "slug",
    "name",
    "positions",
    "age",
    "team",
    "games_played",
    "minutes_played",
    "player_efficiency_rating",
    "true_shooting_percentage",
    "three_point_attempt_rate",
    "free_throw_attempt_rate",
    "offensive_rebound_percentage",
    "defensive_rebound_percentage",
    "total_rebound_percentage",
    "assist_percentage",
    "steal_percentage",
    "block_percentage",
    "turnover_percentage",
    "usage_percentage",
    "offensive_win_shares",
    "defensive_win_shares",
    "win_shares",
    "win_shares_per_48_minutes",
    "offensive_box_plus_minus",
    "defensive_box_plus_minus",
    "box_plus_minus",
    "value_over_replacement_player",
]

TEAM_BOX_SCORES_COLUMN_NAMES = [
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


class WriteOptions:
    def __init__(self, file_path=None, mode=None, custom_options=None):
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
        output_options = self.DEFAULT_OPTIONS \
            if options.custom_options is None \
            else merge_two_dicts(
                first=self.DEFAULT_OPTIONS,
                second=options.custom_options
            )

        if options.should_write_to_file():
            with open(options.file_path, options.mode.value, newline="") as json_file:
                return json.dump(data, json_file, cls=self.encoder, **output_options)

        return json.dumps(data, cls=self.encoder, **output_options)


class CSVWriter:
    def __init__(self, column_names, row_formatter):
        self.column_names = column_names
        self.row_formatter = row_formatter

    def write(self, data, options):
        with open(options.file_path, options.mode.value, newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.column_names)
            writer.writeheader()
            writer.writerows([self.row_formatter.format(row_data) for row_data in data])


class RowFormatter:
    def __init__(self, data_field_names):
        self.data_field_names = data_field_names

    def format(self, row_data):
        return {
            data_field_name: row_data[data_field_name].value
            if data_field_name in ["away_team", "home_team", "team", "location", "opponent", "outcome"]
            else "-".join(map(lambda position: position.value, row_data[data_field_name]))
            if data_field_name == "positions"
            else row_data[data_field_name]
            for data_field_name in self.data_field_names
        }
