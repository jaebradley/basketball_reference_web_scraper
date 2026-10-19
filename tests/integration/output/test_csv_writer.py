import csv
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from basketball_reference_web_scraper.data import OutputType, OutputWriteOption
from basketball_reference_web_scraper.output.writers import CSVWriter, FileOptions, OutputOptions, SearchCSVWriter


class TestCSVWriterFileModes(TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "output.csv"
        self.append_modes = (OutputWriteOption.APPEND, OutputWriteOption.APPEND_AND_WRITE)

    def write(self, rows, mode, writer_type=CSVWriter):
        writer_type(value_formatter=lambda value: value).write(
            data={"players": rows} if writer_type is SearchCSVWriter else rows,
            options=OutputOptions(
                file_options=FileOptions(path=self.path, mode=mode),
                formatting_options={"column_names": ["name"]},
                output_type=OutputType.CSV,
            ),
        )

    def read(self):
        with self.path.open(newline="", encoding="utf8") as output:
            return list(csv.DictReader(output))

    def test_append_preserves_one_header_and_all_rows(self):
        first = [{"name": "Nikola Jokić"}]
        second = [{"name": "Last, First"}]
        for mode in self.append_modes:
            for writer_type in (CSVWriter, SearchCSVWriter):
                with self.subTest(mode=mode, writer_type=writer_type):
                    self.write(first, OutputWriteOption.WRITE, writer_type)
                    self.write(second, mode, writer_type)
                    self.write(first, mode, writer_type)
                    self.assertEqual(first + second + first, self.read())

    def test_append_creates_missing_file_with_header(self):
        rows = [{"name": "Stephen Curry"}]
        for mode in self.append_modes:
            with self.subTest(mode=mode):
                self.path.unlink(missing_ok=True)
                self.write(rows, mode)
                self.assertEqual(rows, self.read())

    def test_append_initializes_empty_file_with_header(self):
        rows = [{"name": "Stephen Curry"}]
        for mode in self.append_modes:
            with self.subTest(mode=mode):
                self.path.write_bytes(b"")
                self.write(rows, mode)
                self.assertEqual(rows, self.read())

    def test_append_empty_batch_preserves_existing_file(self):
        for mode in self.append_modes:
            with self.subTest(mode=mode):
                self.write([{"name": "Stephen Curry"}], OutputWriteOption.WRITE)
                before = self.path.read_bytes()
                self.write([], mode)
                self.assertEqual(before, self.path.read_bytes())

    def test_append_to_header_only_file(self):
        rows = [{"name": "Stephen Curry"}]
        for mode in self.append_modes:
            with self.subTest(mode=mode):
                self.write([], OutputWriteOption.WRITE)
                self.write(rows, mode)
                self.assertEqual(rows, self.read())

    def test_write_modes_replace_existing_file(self):
        rows = [{"name": "Stephen Curry"}]
        for mode in (OutputWriteOption.WRITE, OutputWriteOption.CREATE_AND_WRITE):
            with self.subTest(mode=mode):
                self.write([{"name": "Nikola Jokić"}], OutputWriteOption.WRITE)
                self.write(rows, mode)
                self.assertEqual(rows, self.read())
