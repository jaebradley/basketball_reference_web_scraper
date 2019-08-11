from unittest import TestCase, mock

from basketball_reference_web_scraper.data import OutputWriteOption, OutputType
from basketball_reference_web_scraper.json_encoders import BasketballReferenceJSONEncoder
from basketball_reference_web_scraper.output import output
from basketball_reference_web_scraper.writers import WriteOptions


class TestOutput(TestCase):
    def setUp(self):
        self.values = ["some values"]
        self.output_file_path = "some output file path"
        self.csv_writer = mock.Mock(write=mock.Mock())

    def test_return_values_when_output_type_is_none(self):
        self.assertEqual(
            self.values,
            output(
                values=self.values,
                output_type=None,
                output_file_path=self.output_file_path,
                csv_writer=self.csv_writer,
            ),
        )

    def test_raise_error_when_output_type_is_not_json_or_csv(self):
        self.assertRaisesRegex(
            ValueError,
            "Unknown output type: some other output type",
            output,
            values=self.values,
            output_type="some other output type",
            output_file_path=None,
            csv_writer=None,
        )

    @mock.patch("basketball_reference_web_scraper.output.JSONWriter")
    def test_output_json_when_output_write_option_is_none_and_no_custom_options(
            self,
            mock_json_writer,
    ):
        mock_json_writer_instance = mock.Mock(write=mock.Mock())
        mock_json_writer.return_value = mock_json_writer_instance

        output(
            values=self.values,
            output_type=OutputType.JSON,
            output_file_path=self.output_file_path,
            csv_writer=None,
        )

        mock_json_writer.assert_called_once_with(encoder=BasketballReferenceJSONEncoder)
        mock_json_writer_instance.write.assert_called_once_with(
            data=self.values,
            options=WriteOptions(
                file_path=self.output_file_path,
                mode=OutputWriteOption.WRITE,
                custom_options=None,
            )
        )

    @mock.patch("basketball_reference_web_scraper.output.JSONWriter")
    def test_output_json_when_output_write_option_is_append_and_no_custom_options(
            self,
            mock_json_writer,
    ):
        mock_json_writer_instance = mock.Mock(write=mock.Mock())
        mock_json_writer.return_value = mock_json_writer_instance

        output(
            values=self.values,
            output_type=OutputType.JSON,
            output_file_path=self.output_file_path,
            csv_writer=None,
            output_write_option=OutputWriteOption.APPEND,
        )

        mock_json_writer.assert_called_once_with(encoder=BasketballReferenceJSONEncoder)
        mock_json_writer_instance.write.assert_called_once_with(
            data=self.values,
            options=WriteOptions(
                file_path=self.output_file_path,
                mode=OutputWriteOption.APPEND,
                custom_options=None,
            )
        )

    @mock.patch("basketball_reference_web_scraper.output.JSONWriter")
    def test_output_json_when_output_write_option_is_none_and_custom_options(
            self,
            mock_json_writer,
    ):
        mock_json_writer_instance = mock.Mock(write=mock.Mock())
        mock_json_writer.return_value = mock_json_writer_instance

        output(
            values=self.values,
            output_type=OutputType.JSON,
            output_file_path=self.output_file_path,
            csv_writer=None,
            json_options={
                "jae": "baebae",
                "bae": "jadley",
            },
        )

        mock_json_writer.assert_called_once_with(encoder=BasketballReferenceJSONEncoder)
        mock_json_writer_instance.write.assert_called_once_with(
            data=self.values,
            options=WriteOptions(
                file_path=self.output_file_path,
                mode=OutputWriteOption.WRITE,
                custom_options={
                    "jae": "baebae",
                    "bae": "jadley",
                },
            )
        )

    @mock.patch("basketball_reference_web_scraper.output.JSONWriter")
    def test_output_json_when_output_write_option_is_append_and_custom_options(
            self,
            mock_json_writer,
    ):
        mock_json_writer_instance = mock.Mock(write=mock.Mock())
        mock_json_writer.return_value = mock_json_writer_instance

        output(
            values=self.values,
            output_type=OutputType.JSON,
            output_file_path=self.output_file_path,
            csv_writer=None,
            output_write_option=OutputWriteOption.APPEND,
            json_options={
                "jae": "baebae",
                "bae": "jadley",
            },
        )

        mock_json_writer.assert_called_once_with(encoder=BasketballReferenceJSONEncoder)
        mock_json_writer_instance.write.assert_called_once_with(
            data=self.values,
            options=WriteOptions(
                file_path=self.output_file_path,
                mode=OutputWriteOption.APPEND,
                custom_options={
                    "jae": "baebae",
                    "bae": "jadley",
                },
            )
        )

    def test_output_csv_when_output_write_option_is_none_and_no_custom_options(self):
        csv_writer = mock.Mock(name="csv_writer", write=mock.Mock())
        output(
            values=self.values,
            output_type=OutputType.CSV,
            output_file_path=self.output_file_path,
            csv_writer=csv_writer,
        )

        csv_writer.write.assert_called_once_with(
            data=self.values,
            options=WriteOptions(
                file_path=self.output_file_path,
                mode=OutputWriteOption.WRITE,
            ),
        )

    def test_output_csv_when_output_write_option_is_append_and_no_custom_options(self):
        csv_writer = mock.Mock(name="csv_writer", write=mock.Mock())
        output(
            values=self.values,
            output_type=OutputType.CSV,
            output_file_path=self.output_file_path,
            csv_writer=csv_writer,
            output_write_option=OutputWriteOption.APPEND,
        )

        csv_writer.write.assert_called_once_with(
            data=self.values,
            options=WriteOptions(
                file_path=self.output_file_path,
                mode=OutputWriteOption.APPEND,
            ),
        )

    @mock.patch.object(WriteOptions, 'should_write_to_file')
    def test_raise_error_when_outputting_csv_but_unable_to_write_to_file(self, mock_should_write_to_file):
        mock_should_write_to_file.return_value = False
        csv_writer = mock.Mock(name="csv_writer", write=mock.Mock())
        self.assertRaisesRegex(
            ValueError,
            "CSV output must contain a file path",
            output,
            values=self.values,
            output_type=OutputType.CSV,
            output_file_path=self.output_file_path,
            csv_writer=csv_writer,
        )
