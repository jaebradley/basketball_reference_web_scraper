from unittest import TestCase

from client import get_schedule


class TestGet_schedule(TestCase):
    def test_get_schedule(self):
        result = get_schedule(2018)
        self.assertIsNotNone(result)
