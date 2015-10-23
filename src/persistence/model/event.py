class Event:
    def __init__(self, start_time, visiting_team_name, home_team_name):

        assert start_time is not None
        assert visiting_team_name is not None
        assert home_team_name is not None

        self.start_time = start_time
        self.visiting_team_name = visiting_team_name
        self.home_team_name = home_team_name