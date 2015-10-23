class BoxScoreUrlGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_url(date):
        box_score_url_arguments = {
            'day': date.day,
            'month': date.month,
            'year': date.year
        }
        box_score_url = 'http://www.basketball-reference.com/friv/dailyleaders.cgi?month={month}&day={day}&year={year}'.format(**box_score_url_arguments)
        return box_score_url