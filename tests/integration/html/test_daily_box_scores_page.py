from unittest import TestCase

import requests
from lxml import html

from basketball_reference_web_scraper.html import DailyBoxScoresPage


class TestDailyBoxScoresPage(TestCase):
    def setUp(self):
        response = requests.get('https://www.basketball-reference.com/boxscores/index.fcgi?month=01&day=01&year=2017')
        self.january_01_2017_box_scores = response.text

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
