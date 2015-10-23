class BoxScore:
    def __init__(
            self,
            first_name,
            last_name,
            date,
            team,
            opponent,
            is_home,
            seconds_played,
            field_goals,
            field_goal_attempts,
            three_point_field_goals,
            three_point_field_goal_attempts,
            free_throws,
            free_throw_attempts,
            offensive_rebounds,
            defensive_rebounds,
            total_rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.date = date
        self.team = team
        self.opponent = opponent
        self.is_home = is_home
        self.seconds_played = seconds_played
        self.field_goals = field_goals
        self.field_goal_attempts = field_goal_attempts
        self.three_point_field_goals = three_point_field_goals
        self.three_point_field_goal_attempts = three_point_field_goal_attempts
        self.free_throws = free_throws
        self.free_throw_attempts = free_throw_attempts
        self.offensive_rebounds = offensive_rebounds
        self.defensive_rebounds = defensive_rebounds
        self.total_rebounds = total_rebounds
        self.assists = assists
        self.steals = steals
        self.blocks = blocks
        self.turnovers = turnovers
        self.personal_fouls = personal_fouls
        self.points = points

    def draft_kings_points(self):
        return self.points + self.three_point_field_goals * 0.5 + self.total_rebounds * 1.25 + self.assists * 1.5 + self.steals * 2 + self.blocks * 2 - self.turnovers * 0.5