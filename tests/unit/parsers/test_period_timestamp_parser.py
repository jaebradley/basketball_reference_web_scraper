from unittest import TestCase

from basketball_reference_web_scraper.parser_service import ParserService
from basketball_reference_web_scraper.parsers import PeriodTimestampParser


class TestPeriodTimestampParser(TestCase):
    def setUp(self):
        self.parser = PeriodTimestampParser(timestamp_format=ParserService.PLAY_BY_PLAY_TIMESTAMP_FORMAT)

    def test_less_than_a_minute_to_seconds(self):
        self.assertEqual(32.1, self.parser.to_seconds(timestamp="0:32.1"))

    def test_more_than_a_minute_to_seconds(self):
        self.assertEqual(684.5, self.parser.to_seconds(timestamp="11:24.5"))
