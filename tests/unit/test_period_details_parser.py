from unittest import TestCase
from unittest.mock import patch

from basketball_reference_web_scraper.data import PeriodType
from basketball_reference_web_scraper.parsers import PeriodDetailsParser


class TestPeriodDetailsParser(TestCase):
    def test_is_overtime_is_true_when_period_count_is_greater_than_regulation_periods_count(self):
        parser = PeriodDetailsParser(regulation_periods_count=4)
        self.assertTrue(parser.is_overtime(period_count=5))

    def test_is_overtime_is_false_when_period_count_is_equal_to_regulation_periods_count(self):
        parser = PeriodDetailsParser(regulation_periods_count=4)
        self.assertFalse(parser.is_overtime(period_count=4))

    def test_is_overtime_is_false_when_period_count_is_less_than_regulation_periods_count(self):
        self.assertFalse(PeriodDetailsParser(regulation_periods_count=4).is_overtime(period_count=3))

    @patch.object(PeriodDetailsParser, 'is_overtime')
    def test_parse_period_number_is_period_count_in_regulation(self, mocked_is_overtime):
        mocked_is_overtime.return_value = False
        self.assertEqual(
            PeriodDetailsParser(regulation_periods_count=4).parse_period_number(period_count="some period count"),
            "some period count",
        )

    @patch.object(PeriodDetailsParser, 'is_overtime')
    def test_parse_period_number_is_difference_between_period_count_and_regulation_periods_count(self, mocked_is_overtime):
        mocked_is_overtime.return_value = True
        self.assertEqual(
            PeriodDetailsParser(regulation_periods_count=4).parse_period_number(period_count=5),
            1,
        )

    @patch.object(PeriodDetailsParser, 'is_overtime')
    def test_parse_period_type_is_overtime_when_in_overtime(self, mocked_is_overtime):
        mocked_is_overtime.return_value = True
        self.assertEqual(
            PeriodDetailsParser(regulation_periods_count=4).parse_period_type(period_count="some period count"),
            PeriodType.OVERTIME,
        )

    @patch.object(PeriodDetailsParser, 'is_overtime')
    def test_parse_period_type_is_quarter_when_in_regulation(self, mocked_is_overtime):
        mocked_is_overtime.return_value = False
        self.assertEqual(
            PeriodDetailsParser(regulation_periods_count=4).parse_period_type(period_count="some period count"),
            PeriodType.QUARTER,
        )
