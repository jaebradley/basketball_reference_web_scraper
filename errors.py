class InvalidDate(Exception):
    def __init__(self, day, month, year):
        message = "Date with year set to {year}, month set to {month}, and day set to {day} is invalid"\
            .format(
                year=year,
                month=month,
                day=day,
            )
        super().__init__(message)


class UnknownOutputType(Exception):
    def __init__(self, output_type):
        message = "Output type {output_type} is invalid".format(output_type=output_type)

        super().__init__(message)