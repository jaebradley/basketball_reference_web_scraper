from unittest import TestCase, mock

from basketball_reference_web_scraper.data import OutputWriteOption
from basketball_reference_web_scraper.output.writers import (
    CSVWriter,
    FileOptions,
    OutputOptions,
    OutputType,
)


class TestCSVWriter(TestCase):
    def setUp(self):
        self.DATA = [{"value": "some"}, {"value": "row"}, {"value": "data"}]
        self.COLUMN_NAMES = ["some", "column", "names"]
        self.row_formatter = mock.Mock(side_effect=lambda x: x)
        self.csv_dict_writer = mock.Mock(writeheader=mock.Mock(), writerows=mock.Mock())
        self.writer = CSVWriter(value_formatter=self.row_formatter)

    @mock.patch("csv.DictWriter")
    def test_opens_correct_file(self, mock_csv_dict_writer):
        with mock.patch("builtins.open", mock.mock_open()) as mock_file:
            mock_csv_dict_writer.return_value = self.csv_dict_writer
            self.writer.write(
                data=self.DATA,
                options=OutputOptions(
                    file_options=FileOptions(
                        path="some file path",
                        mode=OutputWriteOption.WRITE,
                    ),
                    formatting_options={"column_names": self.COLUMN_NAMES},
                    output_type=OutputType.CSV,
                ),
            )
            mock_file.assert_called_with(
                "some file path",
                OutputWriteOption.WRITE.value,
                newline="",
                encoding="utf8",
            )

    @mock.patch("csv.DictWriter")
    def test_file_and_columns_are_used_by_writer(self, mock_csv_dict_writer):
        with mock.patch("builtins.open", mock.mock_open()) as mock_file:
            mock_csv_dict_writer.return_value = self.csv_dict_writer
            self.writer.write(
                data=self.DATA,
                options=OutputOptions(
                    file_options=FileOptions(
                        path="some file path",
                        mode=OutputWriteOption.WRITE,
                    ),
                    formatting_options={"column_names": self.COLUMN_NAMES},
                    output_type=OutputType.CSV,
                ),
            )
            mock_csv_dict_writer.assert_called_with(
                mock_file(), fieldnames=self.COLUMN_NAMES
            )

    @mock.patch("csv.DictWriter")
    def test_header_is_written(self, mock_csv_dict_writer):
        with mock.patch("builtins.open", mock.mock_open()):
            mock_csv_dict_writer.return_value = self.csv_dict_writer
            self.writer.write(
                data=self.DATA,
                options=OutputOptions(
                    file_options=FileOptions(
                        path="some file path",
                        mode=OutputWriteOption.WRITE,
                    ),
                    formatting_options={"column_names": self.COLUMN_NAMES},
                    output_type=OutputType.CSV,
                ),
            )
            self.csv_dict_writer.writeheader.assert_called_once_with()

    @mock.patch("csv.DictWriter")
    def test_rows_are_written(self, mock_csv_dict_writer):
        with mock.patch("builtins.open", mock.mock_open()):
            mock_csv_dict_writer.return_value = self.csv_dict_writer
            self.writer.write(
                data=self.DATA,
                options=OutputOptions(
                    file_options=FileOptions(
                        path="some file path",
                        mode=OutputWriteOption.WRITE,
                    ),
                    formatting_options={"column_names": self.COLUMN_NAMES},
                    output_type=OutputType.CSV,
                ),
            )
            self.csv_dict_writer.writerows.assert_called_once_with(
                [{"value": "some"}, {"value": "row"}, {"value": "data"}]
            )

    def test_in_memory_output_returns_csv_string_when_no_file_path(self):
        writer = CSVWriter(value_formatter=lambda value: value)
        output = writer.write(
            data=[{"name": "jaebaebae", "value": 1}],
            options=OutputOptions(
                file_options=FileOptions(path=None, mode=None),
                formatting_options={"column_names": ["name", "value"]},
                output_type=OutputType.CSV,
            ),
        )
        self.assertEqual("name,value\r\njaebaebae,1\r\n", output)

    def test_missing_column_names_raises_value_error(self):
        writer = CSVWriter(value_formatter=lambda value: value)
        with self.assertRaisesRegex(ValueError, "column_names"):
            writer.write(
                data=[{"name": "jaebaebae"}],
                options=OutputOptions(
                    file_options=FileOptions(path=None, mode=None),
                    formatting_options=None,
                    output_type=OutputType.CSV,
                ),
            )

    def test_file_output_returns_none(self):
        writer = CSVWriter(value_formatter=lambda value: value)
        with (
            mock.patch("builtins.open", mock.mock_open()) as mock_file,
            mock.patch("csv.DictWriter") as mock_csv_dict_writer,
        ):
            mock_csv_dict_writer.return_value = self.csv_dict_writer
            result = writer.write(
                data=self.DATA,
                options=OutputOptions(
                    file_options=FileOptions(
                        path="some file path", mode=OutputWriteOption.WRITE
                    ),
                    formatting_options={"column_names": self.COLUMN_NAMES},
                    output_type=OutputType.CSV,
                ),
            )
            mock_file.assert_called_once()
            self.assertIsNone(result)
