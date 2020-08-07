from unittest import TestCase, mock

from basketball_reference_web_scraper.data import OutputType, OutputWriteOption
from basketball_reference_web_scraper.output.service import OutputService
from basketball_reference_web_scraper.output.writers import OutputOptions, FileOptions


class TestOutput(TestCase):
    def setUp(self):
        self.values = ["some values"]
        self.output_file_path = "some output file path"
        self.csv_writer = mock.Mock(write=mock.Mock())
        self.json_writer = mock.Mock(write=mock.Mock())
        self.output_service = OutputService(json_writer=self.json_writer, csv_writer=self.csv_writer)

    def test_return_values_when_output_type_is_none(self):
        self.assertEqual(
            self.values,
            self.output_service.output(
                data=self.values,
                options=OutputOptions(
                    file_options=FileOptions.of(),
                    formatting_options={},
                    output_type=None,
                ),
            ),
        )

    def test_output_json_when_output_write_option_is_none_and_no_custom_options(self):
        options = OutputOptions(
            output_type=OutputType.JSON,
            file_options=FileOptions(path=self.output_file_path, mode=None),
            formatting_options={},
        )
        self.output_service.output(data=self.values, options=options)
        self.json_writer.write.assert_called_once_with(
            data=self.values,
            options=options
        )

    def test_output_json_when_output_write_option_is_append_and_no_custom_options(self):
        options = OutputOptions(
            output_type=OutputType.JSON,
            file_options=FileOptions(path=self.output_file_path, mode=OutputWriteOption.APPEND),
            formatting_options={}
        )

        self.output_service.output(data=self.values, options=options)
        self.json_writer.write.assert_called_once_with(data=self.values, options=options)

    def test_output_json_when_output_write_option_is_none_and_custom_options(self):
        options = OutputOptions(
            output_type=OutputType.JSON,
            file_options=FileOptions(path=self.output_file_path, mode=None),
            formatting_options={
                "jae": "baebae",
                "bae": "jadley",
            }
        )

        self.output_service.output(data=self.values, options=options)
        self.json_writer.write.assert_called_once_with(data=self.values, options=options)

    def test_output_json_when_output_write_option_is_append_and_custom_options(self):
        options = OutputOptions(
            output_type=OutputType.JSON,
            file_options=FileOptions(path=self.output_file_path, mode=OutputWriteOption.APPEND),
            formatting_options={
                "jae": "baebae",
                "bae": "jadley",
            }
        )

        self.output_service.output(data=self.values, options=options)
        self.json_writer.write.assert_called_once_with(data=self.values, options=options)

    def test_output_csv_when_output_write_option_is_none_and_no_custom_options(self):
        options = OutputOptions(
            output_type=OutputType.CSV,
            file_options=FileOptions(path=self.output_file_path, mode=OutputWriteOption.WRITE),
            formatting_options={}
        )

        self.output_service.output(data=self.values, options=options)
        self.csv_writer.write.assert_called_once_with(data=self.values, options=options)

    def test_output_csv_when_output_write_option_is_append_and_no_custom_options(self):
        options = OutputOptions(
            output_type=OutputType.CSV,
            file_options=FileOptions(path=self.output_file_path, mode=OutputWriteOption.APPEND),
            formatting_options={}
        )

        self.output_service.output(data=self.values, options=options)
        self.csv_writer.write.assert_called_once_with(data=self.values, options=options)

    def test_raise_error_when_outputting_csv_but_unable_to_write_to_file(self):
        options = OutputOptions(
            output_type="jaebaebae",
            file_options=FileOptions(path=self.output_file_path, mode=OutputWriteOption.APPEND),
            formatting_options={}
        )
        self.assertRaisesRegex(
            ValueError,
            "Unknown output type: jaebaebae",
            self.output_service.output,
            data=self.values,
            options=options,
        )
