import logging

from basketball_reference_web_scraper.setup_logging import setup_logging


class PlayerSeasonStatisticsUrlGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_url(season_start_year):
        setup_logging()
        logger = logging.getLogger()
        player_season_statistics_url_arguments = {
            'year': season_start_year - 1
        }
        player_season_statistics_url = 'http://www.basketball-reference.com/leagues/NBA_{year}_totals.html?lid=header_seasons'.format(**player_season_statistics_url_arguments)
        logger.info("box score url: {0}".format(player_season_statistics_url))
        return player_season_statistics_url
