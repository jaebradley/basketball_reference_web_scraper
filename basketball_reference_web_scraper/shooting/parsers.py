from shooting.html import PlayerShootingStatisticRow
from utilities import str_to_int, str_to_float


class PlayerSeasonShootingStatisticsParser:
    def __init__(self, position_abbreviation_parser, team_abbreviation_parser):
        self.position_abbreviation_parser = position_abbreviation_parser
        self.team_abbreviation_parser = team_abbreviation_parser

    def parse(self, totals: list[PlayerShootingStatisticRow]):
        return [
            {
                "slug": str(total.slug),
                "name": str(total.name).rstrip("*"),
                "position": self.position_abbreviation_parser.from_abbreviation(total.position_abbreviation),
                "age": str_to_int(total.age, default=None),
                "team": self.team_abbreviation_parser.from_abbreviation(total.team_abbreviation),
                "games_played": str_to_int(total.games_played),
                "games_started": str_to_int(total.games_started),
                "minutes_played": str_to_int(total.minutes_played),
                "field_goal_percentage": str_to_float(total.field_goal_percentage),
                "average_field_goal_attempt_distance": {
                    "value": str_to_float(total.average_field_goal_attempt_distance_in_feet),
                    "units": "feet"
                },
                "two_point_shot_statistics": {
                    "field_goal_percentage": str_to_float(total.two_point_field_goal_percentage),
                    "assisted_percentage": str_to_float(total.percentage_of_two_pointers_that_were_assisted),
                    "percentage_of_total_field_goal_attempts": str_to_float(
                        total.percentage_of_field_goal_attempts_that_were_two_pointers),
                    "statistics_by_range": {
                        "0-3": {
                            "percentage_of_total_field_goal_attempts": str_to_float(
                                total.percentage_of_field_goal_attempts_zero_to_three_feet_from_the_basket),
                            "field_goal_percentage": str_to_float(
                                total.zero_to_three_feet_from_the_basket_field_goal_percentage),
                            "units": "feet"
                        },
                        "3-10": {
                            "percentage_of_total_field_goal_attempts": str_to_float(
                                total.percentage_of_field_goal_attempts_three_to_ten_feet_from_the_basket),
                            "field_goal_percentage": str_to_float(
                                total.three_to_ten_feet_from_the_basket_field_goal_percentage),
                            "units": "feet"
                        },
                        "10-16": {
                            "percentage_of_total_field_goal_attempts": str_to_float(
                                total.percentage_of_field_goal_attempts_ten_to_sixteen_feet_from_the_basket),
                            "field_goal_percentage": str_to_float(
                                total.ten_to_sixteen_feet_from_the_basket_field_goal_percentage),
                            "units": "feet"
                        },
                        "16+": {
                            "percentage_of_total_field_goal_attempts": str_to_float(
                                total.percentage_of_field_goal_attempts_sixteen_feet_from_the_basket_to_three_point_line),
                            "field_goal_percentage": str_to_float(
                                total.sixteen_to_three_point_line_field_goal_percentage),
                            "units": "feet"
                        }
                    },
                    "dunks": {
                        "percentage_of_total_field_goal_attempts": str_to_float(
                            total.percentage_of_field_goal_attempts_that_were_dunks),
                        "made": str_to_int(total.made_dunks),
                    }
                },
                "three_point_shot_statistics": {
                    "field_goal_percentage": str_to_float(total.three_point_field_goal_percentage),
                    "assisted_percentage": str_to_float(total.percentage_of_three_pointers_that_were_assisted),
                    "percentage_of_total_field_goal_attempts": str_to_float(
                        total.percentage_of_field_goal_attempts_that_were_three_pointers),
                    "corner": {
                        "percentage_of_three_point_field_goal_attempts": str_to_float(
                            total.percentage_of_three_point_attempts_that_were_corner_threes),
                        "field_goal_percentage": str_to_float(total.corner_three_field_goal_percentage)
                    },
                    "beyond_half_court": {
                        "attempts": str_to_int(total.beyond_half_court_attempts),
                        "made": str_to_int(total.made_beyond_half_court_shots)
                    }
                },
            } for total in totals
        ]
