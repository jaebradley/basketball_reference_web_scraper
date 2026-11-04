from unittest import TestCase

from basketball_reference_web_scraper.utilities import (
    str_to_int,
    str_to_float,
    merge_two_dicts,
)


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

    def test_none_returns_default(self):
        self.assertEqual(0, str_to_int(None))
        self.assertIsNone(str_to_int(None, default=None))


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

    def test_none_returns_default(self):
        self.assertEqual(0.0, str_to_float(None))
        self.assertIsNone(str_to_float(None, default=None))

    def test_nan_returns_default(self):
        self.assertEqual(0.0, str_to_float("NaN"))
        self.assertIsNone(str_to_float("NaN", default=None))

    def test_infinity_returns_default(self):
        self.assertEqual(0.0, str_to_float("inf"))
        self.assertEqual(0.0, str_to_float("-inf"))
        self.assertIsNone(str_to_float("Infinity", default=None))


class TestMergeTwoDicts(TestCase):
    def test_merges_two_empty_dicts(self):
        self.assertEqual({}, merge_two_dicts({}, {}))

    def test_merges_empty_dict_with_non_empty_dict(self):
        self.assertEqual({"jae": "baebae"}, merge_two_dicts({}, {"jae": "baebae"}))

    def test_merges_non_empty_dict_with_empty_dict(self):
        self.assertEqual({"jae": "baebae"}, merge_two_dicts({"jae": "baebae"}, {}))

    def test_merge_non_empty_dicts_with_unique_keys(self):
        self.assertEqual(
            {"jae": "baebae", "bae": "jadley"},
            merge_two_dicts({"jae": "baebae"}, {"bae": "jadley"}),
        )

    def test_merge_non_empty_dicts_with_shared_keys(self):
        self.assertEqual(
            {"jae": "baebae2"}, merge_two_dicts({"jae": "baebae"}, {"jae": "baebae2"})
        )
