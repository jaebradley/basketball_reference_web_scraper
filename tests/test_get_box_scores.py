from unittest import TestCase

from http_client import get_box_scores


class TestGet_box_scores(TestCase):
    def test_get_box_scores(self):
        result = get_box_scores(day=1, month=1, year=2018)
        self.assertIsNotNone(result)

    def test_get_box_scores_for_day_that_does_not_exist(self):
        result = get_box_scores(day=-1, month=1, year=2018)
        self.assertIsNotNone(result)

