import csv
import json

from basketball_reference_web_scraper.data import OutputType, OutputWriteOption

box_score_fieldname = [
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

game_fieldname = [
    "start_time",
    "away_team",
    "away_team_score",
    "home_team",
    "home_team_score",
]

player_season_totals_fieldname = [
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

player_season_advanced_fieldname = [
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
    "offensive_box_plus/minus",
    "defensive_box_plus/minus",
    "box_plus/minus",
    "value_over_replacement_player",
]

team_box_score_fieldname = [
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

default_json_options = {
    "sort_keys": True,
    "indent": 4,
}


def merge_two_dicts(first, second):
    combined = first.copy()
    combined.update(second)
    return combined


def output(values, output_type, output_file_path, encoder, csv_writer, output_write_option=None, json_options=None):
    if output_type is None:
        return values

    write_option = OutputWriteOption.WRITE if output_write_option is None else output_write_option

    if output_type == OutputType.JSON:
        options = default_json_options if json_options is None else merge_two_dicts(first=default_json_options, second=json_options)
        if output_file_path is None:
            return json.dumps(values, cls=encoder, **options)
        else:
            with open(output_file_path, write_option.value, newline="") as json_file:
                return json.dump(values, json_file, cls=encoder, **options)

    if output_type == OutputType.CSV:
        if output_file_path is None:
            raise ValueError("CSV output must contain a file path")
        else:
            return csv_writer(rows=values, output_file_path=output_file_path, write_option=write_option)

    raise ValueError("Unknown output type: {output_type}".format(output_type=output_type))

# I wrote the explicit mapping of CSV values because there didn't seem to be a way of outputting the values of enums
# without doing it this way


def box_scores_to_csv(rows, output_file_path, write_option):
    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=box_score_fieldname)
        writer.writeheader()
        writer.writerows(
            {
                "slug": row["slug"],
                "name": row["name"],
                "team": row["team"].value,
                "location": row["location"].value,
                "opponent": row["opponent"].value,
                "outcome": row["outcome"].value,
                "seconds_played": row["seconds_played"],
                "made_field_goals": row["made_field_goals"],
                "attempted_field_goals": row["attempted_field_goals"],
                "made_three_point_field_goals": row["made_three_point_field_goals"],
                "attempted_three_point_field_goals": row["attempted_three_point_field_goals"],
                "made_free_throws": row["made_free_throws"],
                "attempted_free_throws": row["attempted_free_throws"],
                "offensive_rebounds": row["offensive_rebounds"],
                "defensive_rebounds": row["defensive_rebounds"],
                "assists": row["assists"],
                "steals": row["steals"],
                "blocks": row["blocks"],
                "turnovers": row["turnovers"],
                "personal_fouls": row["personal_fouls"],
                "game_score": row["game_score"],
            } for row in rows
        )


def schedule_to_csv(rows, output_file_path, write_option):
    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=game_fieldname)
        writer.writeheader()
        writer.writerows(
            {
                "start_time": row["start_time"],
                "away_team": row["away_team"].value,
                "away_team_score": row["away_team_score"],
                "home_team": row["home_team"].value,
                "home_team_score": row["home_team_score"],
            } for row in rows
        )


def players_season_totals_to_csv(rows, output_file_path, write_option):
    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=player_season_totals_fieldname)
        writer.writeheader()
        writer.writerows(
            {
                "slug": row["slug"],
                "name": row["name"],
                "positions": "-".join(map(lambda position: position.value, row["positions"])),
                "age": row["age"],
                "team": row["team"].value,
                "games_played": row["games_played"],
                "games_started": row["games_started"],
                "minutes_played": row["minutes_played"],
                "made_field_goals": row["made_field_goals"],
                "attempted_field_goals": row["attempted_field_goals"],
                "made_three_point_field_goals": row["made_three_point_field_goals"],
                "attempted_three_point_field_goals": row["attempted_three_point_field_goals"],
                "made_free_throws": row["made_free_throws"],
                "attempted_free_throws": row["attempted_free_throws"],
                "offensive_rebounds": row["offensive_rebounds"],
                "defensive_rebounds": row["defensive_rebounds"],
                "assists": row["assists"],
                "steals": row["steals"],
                "blocks": row["blocks"],
                "turnovers": row["turnovers"],
                "personal_fouls": row["personal_fouls"],
            } for row in rows
        )


def players_season_advanced_to_csv(rows, output_file_path, write_option):
    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=player_season_advanced_fieldname)
        writer.writeheader()
        writer.writerows(
            {
                "slug": row["slug"],
                "name": row["name"],
                "positions": "-".join(map(lambda position: position.value, row["positions"])),
                "age": row["age"],
                "team": row["team"].value,
                "games_played": row["games_played"],
                "minutes_played": row["minutes_played"],
                "player_efficiency_rating": row["player_efficiency_rating"],
                "true_shooting_percentage": row["true_shooting_percentage"],
                "three_point_attempt_rate": row["three_point_attempt_rate"],
                "free_throw_attempt_rate": row["free_throw_attempt_rate"],
                "offensive_rebound_percentage": row["offensive_rebound_percentage"],
                "defensive_rebound_percentage": row["defensive_rebound_percentage"],
                "total_rebound_percentage": row["total_rebound_percentage"],
                "assist_percentage": row["assist_percentage"],
                "steal_percentage": row["steal_percentage"],
                "block_percentage": row["block_percentage"],
                "turnover_percentage": row["turnover_percentage"],
                "usage_percentage": row["usage_percentage"],
                "offensive_win_shares": row["offensive_win_shares"],
                "defensive_win_shares": row["defensive_win_shares"],
                "win_shares": row["win_shares"],
                "win_shares_per_48_minutes": row["win_shares_per_48_minutes"],
                "offensive_box_plus/minus": row["offensive_box_plus/minus"],
                "defensive_box_plus/minus": row["defensive_box_plus/minus"],
                "box_plus/minus": row["box_plus/minus"],
                "value_over_replacement_player": row["value_over_replacement_player"],
            } for row in rows
        )


def team_box_scores_to_csv(rows, output_file_path, write_option):
    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=team_box_score_fieldname)
        writer.writeheader()
        writer.writerows(
            {
                "team": row["team"].value,
                "minutes_played": row["minutes_played"],
                "made_field_goals": row["made_field_goals"],
                "attempted_field_goals": row["attempted_field_goals"],
                "made_three_point_field_goals": row["made_three_point_field_goals"],
                "attempted_three_point_field_goals": row["attempted_three_point_field_goals"],
                "made_free_throws": row["made_free_throws"],
                "attempted_free_throws": row["attempted_free_throws"],
                "offensive_rebounds": row["offensive_rebounds"],
                "defensive_rebounds": row["defensive_rebounds"],
                "assists": row["assists"],
                "steals": row["steals"],
                "blocks": row["blocks"],
                "turnovers": row["turnovers"],
                "personal_fouls": row["personal_fouls"],
            } for row in rows
        )
