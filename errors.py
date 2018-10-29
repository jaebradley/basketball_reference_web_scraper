class InvalidDate(Exception):
    def __init__(self, day, month, year):
        message = "Date with year set to {year}, month set to {month}, and day set to {day} is invalid"\
            .format(
                year=year,
                month=month,
                day=day,
            )
        super().__init__(message)
