import re
from datetime import datetime

from basketball_reference_web_scraper.data import PeriodType
from basketball_reference_web_scraper.utilities import str_to_int, str_to_float


class TeamAbbreviationParser:
    def __init__(self, abbreviations_to_teams):
        self.abbreviations_to_teams = abbreviations_to_teams

    def from_abbreviation(self, abbreviation):
        return self.abbreviations_to_teams.get(abbreviation)


class PositionAbbreviationParser:
    def __init__(self, abbreviations_to_positions):
        self.abbreviations_to_positions = abbreviations_to_positions

    def from_abbreviation(self, abbreviation):
        return self.abbreviations_to_positions.get(abbreviation)

    def from_abbreviations(self, abbreviations):
        parsed_positions = list(
            map(
                lambda position_abbreviation: self.from_abbreviation(position_abbreviation),
                abbreviations.split("-")
            )
        )
        return [position for position in parsed_positions if position is not None]


class LocationAbbreviationParser:
    def __init__(self, abbreviations_to_locations):
        self.abbreviations_to_locations = abbreviations_to_locations

    def from_abbreviation(self, abbreviation):
        location = self.abbreviations_to_locations.get(abbreviation)
        if location is None:
            raise ValueError("Unknown symbol: {location}".format(location=location))

        return location


class OutcomeAbbreviationParser:
    def __init__(self, abbreviations_to_outcomes):
        self.abbreviations_to_outcomes = abbreviations_to_outcomes

    def from_abbreviation(self, abbreviation):
        outcome = self.abbreviations_to_outcomes.get(abbreviation)
        if outcome is None:
            raise ValueError("Unknown symbol: {outcome}".format(outcome=outcome))

        return outcome


class SecondsPlayedParser:
    def parse(self, formatted_playing_time):
        if formatted_playing_time == "":
            return 0

        # It seems like basketball reference formats everything in MM:SS
        # even when the playing time is greater than 59 minutes, 59 seconds.
        #
        # Because of this, we can't use strptime / %M as valid values are 0-59.
        # So have to parse time by splitting on ":" and assuming that
        # the first part is the minute part and the second part is the seconds part
        time_parts = formatted_playing_time.split(":")
        minutes_played = time_parts[0]
        seconds_played = time_parts[1]
        return 60 * int(minutes_played) + int(seconds_played)


class PeriodDetailsParser:
    def __init__(self, regulation_periods_count):
        self.regulation_periods_count = regulation_periods_count

    def is_overtime(self, period_count):
        return period_count > self.regulation_periods_count

    def parse_period_number(self, period_count):
        if self.is_overtime(period_count=period_count):
            return period_count - self.regulation_periods_count

        return period_count

    def parse_period_type(self, period_count):
        if self.is_overtime(period_count=period_count):
            return PeriodType.OVERTIME

        return PeriodType.QUARTER


class PeriodTimestampParser:
    def __init__(self, timestamp_format):
        self.timestamp_format = timestamp_format

    def to_seconds(self, timestamp):
        dt = datetime.strptime(timestamp, self.timestamp_format)
        return float(
            (dt.minute * 60) + dt.second + (dt.microsecond / 1000000)
        )


class ScoresParser:
    def __init__(
            self,
            scores_regex,
            away_team_score_group_name='away_team_score',
            home_team_score_group_name='home_team_score',
    ):
        self.scores_regex = scores_regex
        self.away_team_score_group_name = away_team_score_group_name
        self.home_team_score_group_name = home_team_score_group_name

    def parse_scores(self, formatted_scores):
        return re.search(self.scores_regex, formatted_scores)

    def parse_away_team_score(self, formatted_scores):
        return int(
            self.parse_scores(formatted_scores=formatted_scores)
                .group(self.away_team_score_group_name)
        )

    def parse_home_team_score(self, formatted_scores):
        return int(
            self.parse_scores(formatted_scores=formatted_scores)
                .group(self.home_team_score_group_name)
        )


class TeamNameParser:
    def __init__(self, teams):
        self.teams = teams

    def parse_team_name(self, team_name):
        return self.teams[team_name.strip().upper().replace(" ", "_")]


class PlayerAdvancedSeasonTotalsParser:
    def __init__(self, position_abbreviation_parser, team_abbreviation_parser):
        self.position_abbreviation_parser = position_abbreviation_parser
        self.team_abbreviation_parser = team_abbreviation_parser

    def parse(self, totals):
        return [
            {
                "slug": str(total.slug),
                "name": str(total.name),
                "positions": self.position_abbreviation_parser.from_abbreviations(total.position_abbreviations),
                "age": str_to_int(total.age, default=None),
                "team": self.team_abbreviation_parser.from_abbreviation(total.team_abbreviation),
                "games_played": str_to_int(total.games_played),
                "minutes_played": str_to_int(total.minutes_played),
                "player_efficiency_rating": str_to_float(total.player_efficiency_rating),
                "true_shooting_percentage": str_to_float(total.true_shooting_percentage),
                "three_point_attempt_rate": str_to_float(total.three_point_attempt_rate),
                "free_throw_attempt_rate": str_to_float(total.free_throw_attempt_rate),
                "offensive_rebound_percentage": str_to_float(total.offensive_rebound_percentage),
                "defensive_rebound_percentage": str_to_float(total.defensive_rebound_percentage),
                "total_rebound_percentage": str_to_float(total.total_rebound_percentage),
                "assist_percentage": str_to_float(total.assist_percentage),
                "steal_percentage": str_to_float(total.steal_percentage),
                "block_percentage": str_to_float(total.block_percentage),
                "turnover_percentage": str_to_float(total.turnover_percentage),
                "usage_percentage": str_to_float(total.usage_percentage),
                "offensive_win_shares": str_to_float(total.offensive_win_shares),
                "defensive_win_shares": str_to_float(total.defensive_win_shares),
                "win_shares": str_to_float(total.win_shares),
                "win_shares_per_48_minutes": str_to_float(total.win_shares_per_48_minutes),
                "offensive_box_plus_minus": str_to_float(total.offensive_plus_minus),
                "defensive_box_plus_minus": str_to_float(total.defensive_plus_minus),
                "box_plus_minus": str_to_float(total.plus_minus),
                "value_over_replacement_player": str_to_float(total.value_over_replacement_player),
            } for total in totals
        ]


class PlayerSeasonTotalsParser:
    def __init__(self, position_abbreviation_parser, team_abbreviation_parser):
        self.position_abbreviation_parser = position_abbreviation_parser
        self.team_abbreviation_parser = team_abbreviation_parser

    def parse(self, totals):
        return [
            {
                "slug": str(total.slug),
                "name": str(total.name),
                "positions": self.position_abbreviation_parser.from_abbreviations(total.position_abbreviations),
                "age": str_to_int(total.age, default=None),
                "team": self.team_abbreviation_parser.from_abbreviation(total.team_abbreviation),
                "games_played": str_to_int(total.games_played),
                "games_started": str_to_int(total.games_started),
                "minutes_played": str_to_int(total.minutes_played),
                "made_field_goals": str_to_int(total.made_field_goals),
                "attempted_field_goals": str_to_int(total.attempted_field_goals),
                "made_three_point_field_goals": str_to_int(total.made_three_point_field_goals),
                "attempted_three_point_field_goals": str_to_int(total.attempted_three_point_field_goals),
                "made_free_throws": str_to_int(total.made_free_throws),
                "attempted_free_throws": str_to_int(total.attempted_free_throws),
                "offensive_rebounds": str_to_int(total.offensive_rebounds),
                "defensive_rebounds": str_to_int(total.defensive_rebounds),
                "assists": str_to_int(total.assists),
                "steals": str_to_int(total.steals),
                "blocks": str_to_int(total.blocks),
                "turnovers": str_to_int(total.turnovers),
                "personal_fouls": str_to_int(total.personal_fouls),
            } for total in totals
        ]


class TeamTotalsParser:
    def __init__(self, team_abbreviation_parser):
        self.team_abbreviation_parser = team_abbreviation_parser

    def parse(self, totals):
        return [
            {
                "team": self.team_abbreviation_parser.from_abbreviation(total.team_abbreviation),
                "minutes_played": str_to_int(total.minutes_played),
                "made_field_goals": str_to_int(total.made_field_goals),
                "attempted_field_goals": str_to_int(total.attempted_field_goals),
                "made_three_point_field_goals": str_to_int(total.made_three_point_field_goals),
                "attempted_three_point_field_goals": str_to_int(total.attempted_three_point_field_goals),
                "made_free_throws": str_to_int(total.made_free_throws),
                "attempted_free_throws": str_to_int(total.attempted_free_throws),
                "offensive_rebounds": str_to_int(total.offensive_rebounds),
                "defensive_rebounds": str_to_int(total.defensive_rebounds),
                "assists": str_to_int(total.assists),
                "steals": str_to_int(total.steals),
                "blocks": str_to_int(total.blocks),
                "turnovers": str_to_int(total.turnovers),
                "personal_fouls": str_to_int(total.personal_fouls),
            } for total in totals
        ]


class PlayerBoxScoresParser:
    def __init__(self, team_abbreviation_parser, location_abbreviation_parser, outcome_abbreviation_parser,
                 seconds_played_parser):
        self.team_abbreviation_parser = team_abbreviation_parser
        self.location_abbreviation_parser = location_abbreviation_parser
        self.outcome_abbreviation_parser = outcome_abbreviation_parser
        self.seconds_played_parser = seconds_played_parser

    def parse(self, box_scores):
        return [
            {
                "slug": str(box_score.slug),
                "name": str(box_score.name),
                "team": self.team_abbreviation_parser.from_abbreviation(box_score.team_abbreviation),
                "location": self.location_abbreviation_parser.from_abbreviation(box_score.location_abbreviation),
                "opponent": self.team_abbreviation_parser.from_abbreviation(box_score.opponent_abbreviation),
                "outcome": self.outcome_abbreviation_parser.from_abbreviation(box_score.outcome),
                "seconds_played": self.seconds_played_parser.parse(box_score.playing_time),
                "made_field_goals": str_to_int(box_score.made_field_goals),
                "attempted_field_goals": str_to_int(box_score.attempted_field_goals),
                "made_three_point_field_goals": str_to_int(box_score.made_three_point_field_goals),
                "attempted_three_point_field_goals": str_to_int(box_score.attempted_three_point_field_goals),
                "made_free_throws": str_to_int(box_score.made_free_throws),
                "attempted_free_throws": str_to_int(box_score.attempted_free_throws),
                "offensive_rebounds": str_to_int(box_score.offensive_rebounds),
                "defensive_rebounds": str_to_int(box_score.defensive_rebounds),
                "assists": str_to_int(box_score.assists),
                "steals": str_to_int(box_score.steals),
                "blocks": str_to_int(box_score.blocks),
                "turnovers": str_to_int(box_score.turnovers),
                "personal_fouls": str_to_int(box_score.personal_fouls),
                "game_score": str_to_float(box_score.game_score),
            } for box_score in box_scores
        ]


class PlayByPlaysParser:
    def __init__(self, period_details_parser, period_timestamp_parser, scores_parser):
        self.period_details_parser = period_details_parser
        self.period_timestamp_parser = period_timestamp_parser
        self.scores_parser = scores_parser

    def parse(self, play_by_plays, away_team, home_team):
        current_period = 0
        result = []
        for play_by_play in play_by_plays:
            if play_by_play.is_start_of_period:
                current_period += 1
            elif play_by_play.has_play_by_play_data:
                result.append(self.format_data(
                    current_period=current_period,
                    play_by_play=play_by_play,
                    away_team=away_team,
                    home_team=home_team,
                ))
        return result

    def format_data(self, current_period, play_by_play, away_team, home_team):
        return {
            "period": self.period_details_parser.parse_period_number(period_count=current_period),
            "period_type": self.period_details_parser.parse_period_type(period_count=current_period),
            "remaining_seconds_in_period": self.period_timestamp_parser.to_seconds(timestamp=play_by_play.timestamp),
            "relevant_team": away_team if play_by_play.is_away_team_play else home_team,
            "away_team": away_team,
            "home_team": home_team,
            "away_score": self.scores_parser.parse_away_team_score(formatted_scores=play_by_play.formatted_scores),
            "home_score": self.scores_parser.parse_home_team_score(formatted_scores=play_by_play.formatted_scores),
            "description": play_by_play.away_team_play_description
            if play_by_play.is_away_team_play
            else play_by_play.home_team_play_description,
        }
