from unittest import TestCase

from basketball_reference_web_scraper.output.writers import FileOptions


class TestFileOptions(TestCase):
    def test_should_write_to_file_is_false_when_type_is_none(self):
        self.assertFalse(FileOptions().should_write_to_file)

    def test_should_write_to_file_is_false_when_nothing_is_defined(self):
        self.assertFalse(FileOptions().should_write_to_file)

    def test_should_write_to_file_is_false_when_file_path_is_not_none_but_mode_is_none(self):
        self.assertFalse(FileOptions(path="some file path", mode=None).should_write_to_file)

    def test_should_write_to_file_is_true_when_output_type_is_not_none_and_file_path_is_not_none_and_mode_is_not_none(self):
        self.assertTrue(FileOptions(path="some file path", mode="some mode").should_write_to_file)

    def test_two_options_with_same_properties_are_equivalent(self):
        self.assertEqual(FileOptions(), FileOptions())

    def test_two_options_with_same_properties_except_file_path_are_not_equivalent(self):
        self.assertNotEqual(FileOptions(path="some file path"), FileOptions())

    def test_two_options_with_same_properties_except_mode_are_not_equivalent(self):
        self.assertNotEqual(FileOptions(mode="some mode"), FileOptions())
