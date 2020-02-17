from unittest import TestCase

from basketball_reference_web_scraper.writers import WriteOptions


class TestWriteOptions(TestCase):
    def test_should_write_to_file_is_false_when_file_path_is_none(self):
        self.assertFalse(WriteOptions(file_path=None).should_write_to_file())

    def test_should_write_to_file_is_false_when_file_path_is_not_none_but_mode_is_none(self):
        self.assertFalse(WriteOptions(file_path="some file path", mode=None).should_write_to_file())

    def test_should_write_to_file_is_true_when_file_path_is_not_none_and_mode_is_not_none(self):
        self.assertTrue(WriteOptions(file_path="some file path", mode="some mode").should_write_to_file())

    def test_two_options_with_same_properties_are_equivalent(self):
        self.assertEqual(WriteOptions(), WriteOptions())

    def test_two_options_with_same_properties_except_file_path_are_not_equivalent(self):
        self.assertNotEqual(WriteOptions(file_path="some file path"), WriteOptions())

    def test_two_options_with_same_properties_except_mode_are_not_equivalent(self):
        self.assertNotEqual(WriteOptions(mode="some mode"), WriteOptions())

    def test_two_options_with_same_properties_except_custom_option_are_not_equivalent(self):
        self.assertNotEqual(WriteOptions(custom_options="some optoins"), WriteOptions())
