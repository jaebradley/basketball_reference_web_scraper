class ScheduleUrlGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_url(year):

        assert year is not None
        assert isinstance(year, int)

        """
        For seasons that span multiple years use greatest year value
        :param year:
        :return:
        """
        return "http://www.basketball-reference.com/leagues/NBA_{0}_games.html".format(year)