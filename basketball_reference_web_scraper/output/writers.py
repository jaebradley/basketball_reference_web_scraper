import csv
import json


class WriteOptions:
    def __init__(self, output_type=None, file_path=None, mode=None, json=None, csv=None):
        self.output_type = output_type
        self.file_path = file_path
        self.mode = mode
        self.json = json
        self.csv = csv

    def should_write_to_file(self):
        return self.output_type is not None and self.file_path is not None and self.mode is not None

    def __eq__(self, other):
        if isinstance(other, WriteOptions):
            return self.output_type == other.output_type \
                   and self.file_path == other.file_path \
                   and self.mode == other.mode \
                   and self.json == other.json \
                   and self.csv == other.csv
        return False


class JSONOptions:
    @staticmethod
    def of(options):
        if options is None:
            return JSONOptions()

        return JSONOptions(sort_keys=options.get("sort_keys"), indent=options.get("indent"))

    def __init__(self, sort_keys=True, indent=4):
        self.sort_keys = sort_keys if sort_keys is not None else True
        self.indent = indent if indent is not None else 4

    def __eq__(self, other):
        if isinstance(other, JSONOptions):
            return self.sort_keys == other.sort_keys \
                    and self.indent == other.indent
        return False


class CSVOptions:
    def __init__(self, column_names):
        self.column_names = column_names

    def __eq__(self, other):
        if isinstance(other, CSVOptions):
            return self.column_names == other.column_names

        return False


class Writer:
    def __init__(self, value_formatter):
        self.value_formatter = value_formatter

    def write(self, data, options):
        raise NotImplementedError()


class JSONWriter(Writer):
    def write(self, data, options):
        if options.should_write_to_file():
            with open(options.file_path, options.mode.value, newline="", encoding="utf8") as json_file:
                return json.dump(data, json_file, cls=self.value_formatter, sort_keys=options.json.sort_keys, indent=options.json.indent)

        return json.dumps(data, cls=self.value_formatter, sort_keys=options.sort_keys, indent=options.indent)


class CSVWriter(Writer):
    def write(self, data, options):
        with open(options.file_path, options.mode.value, newline="", encoding="utf8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=options.csv.column_names)
            writer.writeheader()

            rows = [
                dict((key, self.value_formatter(value)) for key, value in row.items())
                for row in data
            ]
            writer.writerows(rows)

