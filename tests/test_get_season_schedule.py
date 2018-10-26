from unittest import TestCase

from http_client import get_season_schedule


class TestGet_season_schedule(TestCase):
    def test_get_season_schedule(self):
        result = get_season_schedule(2018)
        self.assertIsNotNone(result)
