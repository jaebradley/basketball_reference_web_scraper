class PlayerSeasonStatistics:
    def __init__(
            self,
            first_name,
            last_name,
            age,
            team,
            position,
            games_played,
            games_started,
            minutes_played,
            field_goals_made,
            field_goals_attempted,
            three_point_field_goals_made,
            three_point_field_goals_attempted,
            two_point_field_goals_made,
            two_point_field_goals_attempted,
            free_throws_made,
            free_throws_attempted,
            offensive_rebounds,
            defensive_rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points
    ):
        self.age = age
        self.first_name = first_name
        self.last_name = last_name
        self.team = team
        self.position = position
        self.games_played = games_played
        self.games_started = games_started
        self.minutes_played = minutes_played
        self.field_goals_made = field_goals_made
        self.field_goals_attempted = field_goals_attempted
        self.three_point_field_goals_made = three_point_field_goals_made
        self.three_point_field_goals_attempted = three_point_field_goals_attempted
        self.two_point_field_goals_made = two_point_field_goals_made
        self.two_point_field_goals_attempted = two_point_field_goals_attempted
        self.free_throws_made = free_throws_made
        self.free_throws_attempted = free_throws_attempted
        self.offensive_rebounds = offensive_rebounds
        self.defensive_rebounds = defensive_rebounds
        self.assists = assists
        self.steals = steals
        self.blocks = blocks
        self.turnovers = turnovers
        self.personal_fouls = personal_fouls
        self.points = points