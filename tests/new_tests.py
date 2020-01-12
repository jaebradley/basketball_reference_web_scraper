import basketball_reference_web_scraper.client as client
from basketball_reference_web_scraper.parsers.player_number import parse_player_link, parse_player_number
from basketball_reference_web_scraper import http_client, four_factors


import unittest


class TestAdditions(unittest.TestCase):
    def test_player_number(self):
        self.assertEqual('8', client.get_jersey_number('Zach LaVine'))

    def test_parse_player_link(self):
        # self.assertEqual('walkeke02.html', parse_player_link('Kemba Walker', html))
        pass

    def test_did_player_start(self):
        self.assertEqual(True, client.did_player_start('Zach LaVine', 27, 11, 2019))

    def test_single_player_box_scores(self):
        self.assertEqual('Zach LaVine', client.single_player_box_scores('Zach LaVine', 27, 11, 2019)['name'])

    def test_single_player_season_total(self):
        self.assertEqual('Zach LaVine', client.single_player_season_totals('Zach LaVine', 2020)['name'])

    def test_four_factors(self):
        four_factors.run_four_factors(1)


if __name__ == '__main__':
    unittest.main()
