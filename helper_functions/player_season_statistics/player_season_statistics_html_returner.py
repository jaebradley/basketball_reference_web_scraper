import urllib2
import logging

import lxml.html as html

from basketball_reference_web_scraper.setup_logging import setup_logging


class PlayerSeasonStatisticsHtmlReturner:

    def __init__(self):
        pass

    @staticmethod
    def return_html(player_season_statistics_url):
        setup_logging()
        logging.getLogger()
        logging.info("making call to {0}".format(player_season_statistics_url))
        content = urllib2.urlopen(player_season_statistics_url).read()
        player_season_statistics_html = html.fromstring(content)
        logging.info("received html for {0}".format(player_season_statistics_url))
        return player_season_statistics_html
