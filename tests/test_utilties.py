from unittest import TestCase

from basketball_reference_web_scraper.utilities import str_to_int, str_to_float


class TestStrToInt(TestCase):
    def test_empty_string_is_zero(self):
        self.assertEqual(str_to_int(""), 0)

    def test_whitespace_is_zero(self):
        self.assertEqual(str_to_int("    "), 0)

    def test_stringified_number_is_converted(self):
        self.assertEqual(str_to_int("10"), 10)

    def test_stringified_number_with_leading_whitespace_is_converted(self):
        self.assertEqual(str_to_int("  10"), 10)

    def test_stringified_number_with_trailing_whitespace_is_converted(self):
        self.assertEqual(str_to_int("10    "), 10)

    def test_with_default(self):
        self.assertIsNone(str_to_int("", default=None))


class TestStrToFloat(TestCase):
    def test_empty_string_is_zero(self):
        self.assertEqual(str_to_float(""), 0.0)

    def test_whitespace_is_zero(self):
        self.assertEqual(str_to_float("    "), 0.0)

    def test_stringified_number_is_converted(self):
        self.assertEqual(str_to_float("1.234"), 1.234)

    def test_stringified_number_with_leading_whitespace_is_converted(self):
        self.assertEqual(str_to_float("  1.234"), 1.234)

    def test_stringified_number_with_trailing_whitespace_is_converted(self):
        self.assertEqual(str_to_float("1.234    "), 1.234)

    def test_with_default(self):
        self.assertIsNone(str_to_float("", default=None))
