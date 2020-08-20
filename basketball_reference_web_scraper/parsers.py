import re
from datetime import datetime

import pytz

from basketball_reference_web_scraper.data import PeriodType, Outcome
from basketball_reference_web_scraper.utilities import str_to_int, str_to_float

PLAYER_SEASON_BOX_SCORES_GAME_DATE_FORMAT = '%Y-%m-%d'
PLAYER_SEASON_BOX_SCORES_OUTCOME_REGEX = '(?P<outcome_abbreviation>W|L) \((?P<margin_of_victory>[^)]+)\)'
SEARCH_RESULT_NAME_REGEX = '(?P<name>^[^\(]+)'


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


class LeagueAbbreviationParser:
    def __init__(self, abbreviations_to_league):
        self.abbreviations_to_league = abbreviations_to_league

    def from_abbreviation(self, abbreviation):
        league = self.abbreviations_to_league.get(abbreviation)
        if league is None:
            raise ValueError("Unknown league abbreviation: {abbreviation}".format(abbreviation=abbreviation))

        return league

    def from_abbreviations(self, abbreviations):
        if abbreviations is None:
            return []

        return [
            self.from_abbreviation(abbreviation=league_abbreviation)
            for league_abbreviation in abbreviations.split("/")
        ]


class PlayerBoxScoreOutcomeParser:
    def __init__(self,
                 outcome_abbreviation_parser,
                 formatted_outcome_regex=PLAYER_SEASON_BOX_SCORES_OUTCOME_REGEX,
                 outcome_abbreviation_regex_group_name='outcome_abbreviation',
                 margin_of_victory_regex_group_name='margin_of_victory',
                 ):
        self.outcome_abbreviation_parser = outcome_abbreviation_parser
        self.formatted_outcome_regex = formatted_outcome_regex
        self.outcome_abbreviation_regex_group_name = outcome_abbreviation_regex_group_name
        self.margin_of_victory_regex_group_name = margin_of_victory_regex_group_name

    def search_formatted_outcome(self, formatted_outcome):
        return re.search(self.formatted_outcome_regex, formatted_outcome)

    def parse_outcome_abbreviation(self, formatted_outcome):
        return self.search_formatted_outcome(formatted_outcome=formatted_outcome) \
            .group(self.outcome_abbreviation_regex_group_name)

    def parse_outcome(self, formatted_outcome):
        return self.outcome_abbreviation_parser.from_abbreviation(
            abbreviation=self.parse_outcome_abbreviation(formatted_outcome=formatted_outcome)
        )

    def parse_margin_of_victory(self, formatted_outcome):
        return int(
            self.search_formatted_outcome(formatted_outcome=formatted_outcome)
                .group(self.margin_of_victory_regex_group_name)
        )


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
    def __init__(self, team_names_to_teams):
        self.team_names_to_teams = team_names_to_teams

    def parse_team_name(self, team_name):
        return self.team_names_to_teams[team_name.strip().upper()]


class ScheduledStartTimeParser:
    def __init__(self, time_zone=pytz.utc):
        self.time_zone = time_zone

    def parse_start_time(self, formatted_date, formatted_time_of_day):
        if formatted_time_of_day is not None and formatted_time_of_day not in ["", " "]:
            # Starting in 2018, the start times had a "p" or "a" appended to the end
            # Between 2001 and 2017, the start times had a "pm" or "am"
            #
            # https://www.basketball-reference.com/leagues/NBA_2018_games.html
            # vs.
            # https://www.basketball-reference.com/leagues/NBA_2001_games.html
            is_prior_format = formatted_time_of_day[-2:] == "am" or formatted_time_of_day[-2:] == "pm"

            # If format contains only "p" or "a" add an "m" so it can be parsed by datetime module
            if is_prior_format:
                combined_formatted_time = formatted_date + " " + formatted_time_of_day
            else:
                combined_formatted_time = formatted_date + " " + formatted_time_of_day + "m"

            if is_prior_format:
                start_time = datetime.strptime(combined_formatted_time, "%a, %b %d, %Y %I:%M %p")
            else:
                start_time = datetime.strptime(combined_formatted_time, "%a, %b %d, %Y %I:%M%p")
        else:
            start_time = datetime.strptime(formatted_date, "%a, %b %d, %Y")

        # All basketball reference times seem to be in Eastern
        est = pytz.timezone("US/Eastern")
        localized_start_time = est.localize(start_time)
        return localized_start_time.astimezone(self.time_zone)


class SearchResultNameParser:
    def __init__(self, search_result_name_regex=SEARCH_RESULT_NAME_REGEX, result_name_regex_group_name="name"):
        self.search_result_name_regex = search_result_name_regex
        self.result_name_regex_group_name = result_name_regex_group_name

    def parse(self, search_result_name):
        return re.search(self.search_result_name_regex, search_result_name) \
            .group(self.result_name_regex_group_name) \
            .strip()


class ResourceLocationParser:
    def __init__(self,
                 resource_location_regex,
                 resource_type_regex_group_name="resource_type",
                 resource_identifier_regex_group_name="resource_identifier"):
        self.resource_location_regex = resource_location_regex
        self.resource_type_regex_group_name = resource_type_regex_group_name
        self.resource_identifier_regex_group_name = resource_identifier_regex_group_name

    def search(self, resource_location):
        return re.search(self.resource_location_regex, resource_location)

    def parse_resource_type(self, resource_location):
        return self.search(resource_location=resource_location).group(self.resource_type_regex_group_name)

    def parse_resource_identifier(self, resource_location):
        return self.search(resource_location=resource_location).group(self.resource_identifier_regex_group_name)


class TeamStandingsParser:
    def __init__(self, teams):
        self.teams = teams

    def parse_team(self, formatted_name):
        for team in self.teams:
            if formatted_name.upper().startswith(team.value):
                return team

        return None


class DivisionNameParser:
    def __init__(self, divisions):
        self.divisions = divisions

    def parse_division(self, formatted_name):
        for division in self.divisions:
            if formatted_name.upper() == "{division} DIVISION".format(division=division.value):
                return division

        return None


class ScheduledGamesParser:
    def __init__(self, start_time_parser, team_name_parser):
        self.start_time_parser = start_time_parser
        self.team_name_parser = team_name_parser

    def parse_games(self, games):
        return [
            {
                "start_time": self.start_time_parser.parse_start_time(
                    formatted_date=game.start_date,
                    formatted_time_of_day=game.start_time_of_day,
                ),
                "away_team": self.team_name_parser.parse_team_name(team_name=game.away_team_name),
                "home_team": self.team_name_parser.parse_team_name(team_name=game.home_team_name),
                "away_team_score": str_to_int(value=game.away_team_score, default=None),
                "home_team_score": str_to_int(value=game.home_team_score, default=None),
            }
            for game in games
        ]


class PlayerAdvancedSeasonTotalsParser:
    def __init__(self, position_abbreviation_parser, team_abbreviation_parser):
        self.position_abbreviation_parser = position_abbreviation_parser
        self.team_abbreviation_parser = team_abbreviation_parser

    def parse(self, totals):
        return [
            {
                "slug": str(total.slug),
                "name": str(total.name).rstrip("*"),
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
                "is_combined_totals": total.is_combined_totals,
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
                "name": str(total.name).rstrip("*"),
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
                "points": str_to_int(total.points),
            } for total in totals
        ]


class TeamTotalsParser:
    def __init__(self, team_abbreviation_parser):
        self.team_abbreviation_parser = team_abbreviation_parser

    def parse(self, first_team_totals, second_team_totals):
        return [
            self.parse_totals(
                team_totals=first_team_totals,
                opposing_team_totals=second_team_totals,
            ),
            self.parse_totals(
                team_totals=second_team_totals,
                opposing_team_totals=first_team_totals,
            ),
        ]

    def parse_totals(self, team_totals, opposing_team_totals):
        current_team = self.team_abbreviation_parser.from_abbreviation(team_totals.team_abbreviation)

        if str_to_int(team_totals.points) > str_to_int(opposing_team_totals.points):
            outcome = Outcome.WIN
        elif str_to_int(team_totals.points) < str_to_int(opposing_team_totals.points):
            outcome = Outcome.LOSS
        else:
            outcome = None

        return {
            "team": current_team,
            "outcome": outcome,
            "minutes_played": str_to_int(team_totals.minutes_played),
            "made_field_goals": str_to_int(team_totals.made_field_goals),
            "attempted_field_goals": str_to_int(team_totals.attempted_field_goals),
            "made_three_point_field_goals": str_to_int(team_totals.made_three_point_field_goals),
            "attempted_three_point_field_goals": str_to_int(team_totals.attempted_three_point_field_goals),
            "made_free_throws": str_to_int(team_totals.made_free_throws),
            "attempted_free_throws": str_to_int(team_totals.attempted_free_throws),
            "offensive_rebounds": str_to_int(team_totals.offensive_rebounds),
            "defensive_rebounds": str_to_int(team_totals.defensive_rebounds),
            "assists": str_to_int(team_totals.assists),
            "steals": str_to_int(team_totals.steals),
            "blocks": str_to_int(team_totals.blocks),
            "turnovers": str_to_int(team_totals.turnovers),
            "personal_fouls": str_to_int(team_totals.personal_fouls),
            "points": str_to_int(team_totals.points),
        }


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
                "name": str(box_score.name).rstrip("*"),
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


class PlayerSeasonBoxScoresParser:
    def __init__(self, team_abbreviation_parser, location_abbreviation_parser, outcome_parser, seconds_played_parser):
        self.team_abbreviation_parser = team_abbreviation_parser
        self.location_abbreviation_parser = location_abbreviation_parser
        self.outcome_parser = outcome_parser
        self.seconds_played_parser = seconds_played_parser

    def parse(self, box_scores):
        return [
            {
                "date": datetime.strptime(str(box_score.date), "%Y-%m-%d").date(),
                "team": self.team_abbreviation_parser.from_abbreviation(box_score.team_abbreviation),
                "location": self.location_abbreviation_parser.from_abbreviation(box_score.location_abbreviation),
                "opponent": self.team_abbreviation_parser.from_abbreviation(box_score.opponent_abbreviation),
                "outcome": self.outcome_parser.parse_outcome(formatted_outcome=box_score.outcome),
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
                "points_scored": str_to_int(box_score.points_scored),
                "game_score": str_to_float(box_score.game_score),
                "plus_minus": str_to_int(box_score.plus_minus),
            } for box_score in box_scores
            if box_score.is_active
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


class SearchResultsParser:
    def __init__(self, search_result_name_parser, search_result_location_parser, league_abbreviation_parser):
        self.search_result_name_parser = search_result_name_parser
        self.search_result_location_parser = search_result_location_parser
        self.league_abbreviation_parser = league_abbreviation_parser

    def parse(self, nba_aba_baa_players):
        return {
            "players": [
                {
                    "name": self.search_result_name_parser.parse(search_result_name=result.resource_name),
                    "identifier": self.search_result_location_parser.parse_resource_identifier(
                        resource_location=result.resource_location
                    ),
                    "leagues": set(
                        self.league_abbreviation_parser.from_abbreviations(
                            abbreviations=result.league_abbreviations
                        )
                    ),
                } for result in nba_aba_baa_players
            ]
        }


class PlayerDataParser:
    def __init__(self, search_result_location_parser, league_abbreviation_parser):
        self.search_result_location_parser = search_result_location_parser
        self.league_abbreviation_parser = league_abbreviation_parser

    def parse(self, player):
        return {
            "name": player.name,
            "identifier": self.search_result_location_parser.parse_resource_identifier(
                resource_location=player.resource_location
            ),
            "leagues": set(
                (
                    self.league_abbreviation_parser.from_abbreviation(abbreviation=abbreviation)
                    for abbreviation in player.league_abbreviations
                )
            )
        }


class ConferenceDivisionStandingsParser:
    def __init__(self, division_name_parser, team_standings_parser, divisions_to_conferences):
        self.division_name_parser = division_name_parser
        self.team_standings_parser = team_standings_parser
        self.divisions_to_conferences = divisions_to_conferences

    def parse(self, division_standings):
        current_division = None
        results = []
        for standing in division_standings:
            if standing.is_division_name_row:
                current_division = self.division_name_parser.parse_division(formatted_name=standing.division_name)
            else:
                results.append({
                    "team": self.team_standings_parser.parse_team(formatted_name=standing.team_name),
                    "wins": str_to_int(standing.wins),
                    "losses": str_to_int(standing.losses),
                    "division": current_division,
                    "conference": self.divisions_to_conferences.get(current_division),
                })
        return results
