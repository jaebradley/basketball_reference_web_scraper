import logging

from basketball_reference_web_scraper.setup_logging import setup_logging


class BoxScoreUrlGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_url(date):
        setup_logging()
        logger = logging.getLogger()
        box_score_url_arguments = {
            'day': date.day,
            'month': date.month,
            'year': date.year
        }
        box_score_url = 'http://www.basketball-reference.com/friv/dailyleaders.cgi?month={month}&day={day}&year={year}'.format(**box_score_url_arguments)
        logger.info("box score url: {0}".format(box_score_url))
        return box_score_url