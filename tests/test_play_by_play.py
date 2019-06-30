from unittest import TestCase

from basketball_reference_web_scraper.client import play_by_play
from basketball_reference_web_scraper.data import Team


class TestPlayByPlay(TestCase):
    def test_get_play_by_play(self):
        result = play_by_play(home_team=Team.MILWAUKEE_BUCKS, day=27, month=10, year=2018)
        self.assertIsNotNone(result)
