import logging


class ScheduleUrlGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_url(year):

        assert year is not None
        assert isinstance(year, int)

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        """
        For seasons that span multiple years use greatest year value
        :param year:
        :return:
        """
        schedule_url = "http://www.basketball-reference.com/leagues/NBA_{0}_games.html".format(year)
        logger.log("schedule url: {0}".format(schedule_url))
        return schedule_url