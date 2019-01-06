from unittest import TestCase
import os

from basketball_reference_web_scraper.parsers.box_scores.games import parse_game_url_paths

january_01_2017_html = os.path.join(os.path.dirname(__file__), './01_01_2017_box_scores.html')


class TestParseGameUrls(TestCase):
    def setUp(self):
        self.january_01_2017_box_scores = open(january_01_2017_html).read()

    def test_parse_urls(self):
        urls = parse_game_url_paths(self.january_01_2017_box_scores)
        self.assertEqual(len(urls), 5)
        self.assertEqual(urls[0], '/boxscores/201701010ATL.html')
        self.assertEqual(urls[1], '/boxscores/201701010IND.html')
        self.assertEqual(urls[2], '/boxscores/201701010LAL.html')
        self.assertEqual(urls[3], '/boxscores/201701010MIA.html')
        self.assertEqual(urls[4], '/boxscores/201701010MIN.html')
