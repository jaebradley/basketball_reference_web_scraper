# I wrote the explicit mapping of CSV values because there didn't seem to be a way of outputting the values of enums
# without doing it this way

SHARED_COLUMN_NAMES = [
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

BOX_SCORE_COLUMN_NAMES = ["slug", "name"] + SHARED_COLUMN_NAMES

PLAYER_SEASON_BOX_SCORE_COLUMN_NAMES = ["date", "points_scored", "plus_minus"] + SHARED_COLUMN_NAMES

SCHEDULE_COLUMN_NAMES = [
    "start_time",
    "away_team",
    "away_team_score",
    "home_team",
    "home_team_score",
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
    "points"
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
    "is_combined_totals",
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
    "points",
    "outcome",
]

PLAY_BY_PLAY_COLUMN_NAMES = [
    "period",
    "period_type",
    "remaining_seconds_in_period",
    "relevant_team",
    "away_team",
    "home_team",
    "away_score",
    "home_score",
    "description",
]

SEARCH_RESULTS_COLUMN_NAMES = [
    "name",
    "identifier",
    "leagues",
]

STANDINGS_COLUMNS_NAMES = [
    "team",
    "wins",
    "losses",
    "division",
    "conference",
]
