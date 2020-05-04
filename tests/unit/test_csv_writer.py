from unittest import TestCase, mock

from basketball_reference_web_scraper.data import OutputWriteOption
from basketball_reference_web_scraper.writers import CSVWriter, WriteOptions


class TestCSVWriter(TestCase):
    DATA = ["some", "row", "data"]
    COLUMN_NAMES = ["some", "column", "names"]

    @mock.patch("basketball_reference_web_scraper.writers.csv.DictWriter")
    def test_opens_correct_file(self, mock_csv_dict_writer):
        with mock.patch("builtins.open", mock.mock_open()) as mock_file:
            csv_dict_writer = mock.Mock(wrteheader=mock.Mock(), writerows=mock.Mock())
            mock_csv_dict_writer.return_value = csv_dict_writer
            row_formatter = mock.Mock(format=mock.Mock())
            csv_dict_writer = mock.Mock(wrteheader=mock.Mock(), writerows=mock.Mock())
            mock_csv_dict_writer.return_value = csv_dict_writer
            writer = CSVWriter(column_names=self.COLUMN_NAMES, row_formatter=row_formatter)
            writer.write(
                data=self.DATA,
                options=WriteOptions(
                    file_path="some file path",
                    mode=OutputWriteOption.WRITE
                )
            )
            mock_file.assert_called_with("some file path", OutputWriteOption.WRITE.value, newline="", encoding="utf8")

    @mock.patch("basketball_reference_web_scraper.writers.csv.DictWriter")
    def test_file_and_columns_are_used_by_writer(self, mock_csv_dict_writer):
        with mock.patch("builtins.open", mock.mock_open()) as mock_file:
            csv_dict_writer = mock.Mock(wrteheader=mock.Mock(), writerows=mock.Mock())
            mock_csv_dict_writer.return_value = csv_dict_writer
            row_formatter = mock.Mock(format=mock.Mock())
            csv_dict_writer = mock.Mock(wrteheader=mock.Mock(), writerows=mock.Mock())
            mock_csv_dict_writer.return_value = csv_dict_writer
            writer = CSVWriter(column_names=self.COLUMN_NAMES, row_formatter=row_formatter)
            writer.write(
                data=self.DATA,
                options=WriteOptions(
                    file_path="some file path",
                    mode=OutputWriteOption.WRITE
                )
            )
            mock_csv_dict_writer.assert_called_with(mock_file(), fieldnames=self.COLUMN_NAMES)

    @mock.patch("basketball_reference_web_scraper.writers.csv.DictWriter")
    def test_header_is_written(self, mock_csv_dict_writer):
        csv_dict_writer = mock.Mock(wrteheader=mock.Mock(), writerows=mock.Mock())
        mock_csv_dict_writer.return_value = csv_dict_writer
        row_formatter = mock.Mock(format=mock.Mock())
        csv_dict_writer = mock.Mock(wrteheader=mock.Mock(), writerows=mock.Mock())
        mock_csv_dict_writer.return_value = csv_dict_writer
        writer = CSVWriter(column_names=self.COLUMN_NAMES, row_formatter=row_formatter)
        writer.write(
            data=self.DATA,
            options=WriteOptions(
                file_path="some file path",
                mode=OutputWriteOption.WRITE
            )
        )
        csv_dict_writer.writeheader.assert_called_once_with()

    @mock.patch("basketball_reference_web_scraper.writers.csv.DictWriter")
    def test_rows_are_written(self, mock_csv_dict_writer):
        csv_dict_writer = mock.Mock(wrteheader=mock.Mock(), writerows=mock.Mock())
        mock_csv_dict_writer.return_value = csv_dict_writer
        row_formatter = mock.Mock(format=mock.Mock())
        csv_dict_writer = mock.Mock(wrteheader=mock.Mock(), writerows=mock.Mock())
        mock_csv_dict_writer.return_value = csv_dict_writer
        writer = CSVWriter(column_names=self.COLUMN_NAMES, row_formatter=row_formatter)
        writer.write(
            data=self.DATA,
            options=WriteOptions(
                file_path="some file path",
                mode=OutputWriteOption.WRITE
            )
        )
        csv_dict_writer.writerows.assert_called_once_with(mock.ANY)
        self.assertEqual(3, row_formatter.format.call_count)
        row_formatter.format.assert_has_calls(
            calls=[
                mock.call("some"),
                mock.call("row"),
                mock.call("data"),
            ],
            any_order=False
        )
