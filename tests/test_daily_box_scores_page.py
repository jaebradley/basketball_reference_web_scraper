import os
from unittest import TestCase

from lxml import html

from basketball_reference_web_scraper.html import DailyBoxScoresPage

january_01_2017_html = os.path.join(os.path.dirname(__file__), './01_01_2017_box_scores.html')


class TestDailyBoxScoresPage(TestCase):
    def setUp(self):
        self.january_01_2017_box_scores_file = open(january_01_2017_html)
        self.january_01_2017_box_scores = self.january_01_2017_box_scores_file.read()

    def tearDown(self):
        self.january_01_2017_box_scores_file.close()

    def test_parse_urls(self):
        page = DailyBoxScoresPage(html=html.fromstring(self.january_01_2017_box_scores))
        urls = page.game_url_paths
        self.assertEqual(len(urls), 5)
        self.assertEqual(urls[0], '/boxscores/201701010ATL.html')
        self.assertEqual(urls[1], '/boxscores/201701010IND.html')
        self.assertEqual(urls[2], '/boxscores/201701010LAL.html')
        self.assertEqual(urls[3], '/boxscores/201701010MIA.html')
        self.assertEqual(urls[4], '/boxscores/201701010MIN.html')
