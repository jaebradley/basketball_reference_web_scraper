import urllib2
import lxml.html as html
import logging
from src.setup_logging import setup_logging


class BoxScoresHtmlReturner:

    def __init__(self):
        pass

    @staticmethod
    def return_html(box_score_url):
        setup_logging()
        logging.getLogger()
        logging.info("making call to {0}".format(box_score_url))
        content = urllib2.urlopen(box_score_url).read()
        box_score_html = html.fromstring(content)
        logging.info("received html for {0}".format(box_score_url))
        return box_score_html