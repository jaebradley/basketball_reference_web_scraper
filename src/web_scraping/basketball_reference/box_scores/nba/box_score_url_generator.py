import logging


class BoxScoreUrlGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_url(date):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        box_score_url_arguments = {
            'day': date.day,
            'month': date.month,
            'year': date.year
        }
        box_score_url = 'http://www.basketball-reference.com/friv/dailyleaders.cgi?month={month}&day={day}&year={year}'.format(**box_score_url_arguments)
        logger.log("box score url: {0}".format(box_score_url))
        return box_score_url