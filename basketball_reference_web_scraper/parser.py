from basketball_reference_web_scraper.utilities import str_to_int


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

