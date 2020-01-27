class InvalidDate(Exception):
    def __init__(self, day, month, year):
        message = "Date with year set to {year}, month set to {month}, and day set to {day} is invalid"\
            .format(
                year=year,
                month=month,
                day=day,
            )
        super().__init__(message)


class InvalidSeason(Exception):
    def __init__(self, season_end_year):
        message = "Season end year of {season_end_year} is invalid".format(season_end_year=season_end_year)
        super().__init__(message)


class InvalidPlayerAndSeason(Exception):
    def __init__(self, player_identifier, season_end_year):
        message = "Player with identifier \"{player_identifier}\" in season ending in {season_end_year} is invalid" \
            .format(player_identifier=player_identifier, season_end_year=season_end_year)
        super().__init__(message)
