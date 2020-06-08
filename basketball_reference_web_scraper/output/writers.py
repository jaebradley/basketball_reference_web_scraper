import csv
import json

from basketball_reference_web_scraper.data import OutputType, OutputWriteOption
from basketball_reference_web_scraper.utilities import merge_two_dicts

DEFAULT_JSON_SORT_KEYS = True
DEFAULT_JSON_INDENT = 4
DEFAULT_JSON_OPTIONS = {
    "sort_keys": DEFAULT_JSON_SORT_KEYS,
    "indent": DEFAULT_JSON_INDENT,
}


class FileOptions:
    @staticmethod
    def of(path=None, mode=None):
        if mode is None:
            return FileOptions(path=path, mode=OutputWriteOption.WRITE)
        
        return FileOptions(path=path, mode=mode)
    
    def __init__(self, path, mode):
        self.path = path
        self.mode = mode

    @property
    def should_write_to_file(self):
        return self.path is not None and self.mode is not None

    def __eq__(self, other):
        if isinstance(other, FileOptions):
            return self.path == other.path \
                   and self.mode == other.mode
        return False


class OutputOptions:
    @staticmethod
    def of(file_options, output_type, json_options=None, csv_options=None):
        if output_type == OutputType.JSON:
            if json_options is None:
                formatting_options = DEFAULT_JSON_OPTIONS
            else:
                formatting_options = merge_two_dicts(DEFAULT_JSON_OPTIONS, json_options)
        elif output_type == OutputType.CSV:
            formatting_options = csv_options
        elif output_type is None:
            return OutputOptions(file_options=None, formatting_options={}, output_type=None)
        else:
            raise ValueError("Unknown output type: {output_type}".format(output_type=output_type))

        return OutputOptions(
            file_options=file_options,
            formatting_options=formatting_options,
            output_type=output_type,
        )

    def __init__(self, file_options, formatting_options, output_type):
        self.file_options = file_options
        self.formatting_options = formatting_options
        self.output_type = output_type

    def __eq__(self, other):
        if isinstance(other, OutputOptions):
            return self.file_options == other.file_options \
                    and self.formatting_options == other.formatting_options \
                    and self.output_type == other.output_type

        return False


class Writer:
    def __init__(self, value_formatter):
        self.value_formatter = value_formatter

    def write(self, data, options):
        raise NotImplementedError()


class JSONWriter(Writer):
    def write(self, data, options):
        output_options = merge_two_dicts(DEFAULT_JSON_OPTIONS, options.formatting_options)
        if options.file_options.should_write_to_file:
            with open(
                    options.file_options.path,
                    options.file_options.mode.value,
                    newline="",
                    encoding="utf8"
            ) as json_file:
                return json.dump(
                    data,
                    json_file,
                    cls=self.value_formatter,
                    **output_options,
                )

        return json.dumps(
            data,
            cls=self.value_formatter,
            **output_options,
        )


class CSVWriter(Writer):
    def rows(self, data):
        return [
            dict((key, self.value_formatter(value)) for key, value in row.items())
            for row in data
        ]

    def write(self, data, options):
        with open(
                options.file_options.path,
                options.file_options.mode.value,
                newline="",
                encoding="utf8",
        ) as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=options.formatting_options.get("column_names"),
            )
            writer.writeheader()

            writer.writerows(self.rows(data=data))


class SearchCSVWriter(CSVWriter):
    def rows(self, data):
        return [
            dict((key, self.value_formatter(value)) for key, value in row.items())
            for row in data["players"]
        ]

