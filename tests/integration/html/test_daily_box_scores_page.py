import os
from unittest import TestCase

from lxml import html

from basketball_reference_web_scraper.html import DailyBoxScoresPage


class TestDailyBoxScoresPage(TestCase):
    def setUp(self):
        with open(os.path.join(
                os.path.dirname(__file__),
                "../files/boxscores/2017/1/1.html"
        ), 'r') as file_input: self.january_01_2017_box_scores = file_input.read()

    def test_game_url_paths_query(self):
        page = DailyBoxScoresPage(html=html.fromstring(self.january_01_2017_box_scores))
        self.assertEqual(page.game_url_paths_query, '//td[contains(@class, "gamelink")]/a')

    def test_parse_urls(self):
        page = DailyBoxScoresPage(html=html.fromstring(self.january_01_2017_box_scores))
        urls = page.game_url_paths
        self.assertEqual(len(urls), 5)
        self.assertEqual(urls[0], '/boxscores/201701010ATL.html')
        self.assertEqual(urls[1], '/boxscores/201701010IND.html')
        self.assertEqual(urls[2], '/boxscores/201701010LAL.html')
        self.assertEqual(urls[3], '/boxscores/201701010MIA.html')
        self.assertEqual(urls[4], '/boxscores/201701010MIN.html')
