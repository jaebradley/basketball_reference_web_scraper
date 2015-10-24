import logging

from basketball_reference_web_scraper.setup_logging import setup_logging


class ScheduleUrlGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_url(year):

        assert year is not None
        assert isinstance(year, int)

        setup_logging()
        logger = logging.getLogger("main")
        """
        For seasons that span multiple years use greatest year value
        :param year:
        :return:
        """
        schedule_url = "http://www.basketball-reference.com/leagues/NBA_{0}_games.html".format(year)
        logger.info("schedule url: {0}".format(schedule_url))
        return schedule_url