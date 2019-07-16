import csv

from basketball_reference_web_scraper.data import OutputType, OutputWriteOption
from basketball_reference_web_scraper.json_encoders import BasketballReferenceJSONEncoder
from basketball_reference_web_scraper.writers import JSONWriter, WriteOptions

play_by_play_fieldname = [
    "quarter",
    "timestamp",
    "side",
    "away_score",
    "home_score",
    "description"
]

default_json_options = {
    "sort_keys": True,
    "indent": 4,
}


def output(values, output_type, output_file_path, csv_writer, output_write_option=None, json_options=None):
    if output_type is None:
        return values

    write_option = OutputWriteOption.WRITE if output_write_option is None else output_write_option

    if output_type == OutputType.JSON:
        options = WriteOptions(file_path=output_file_path, mode=write_option, custom_options=json_options)
        writer = JSONWriter(encoder=BasketballReferenceJSONEncoder)
        return writer.write(data=values, options=options)

    if output_type == OutputType.CSV:
        options = WriteOptions(file_path=output_file_path, mode=write_option)
        if options.should_write_to_file():
            return csv_writer.write(data=values, options=options)
        else:
            raise ValueError("CSV output must contain a file path")

    raise ValueError("Unknown output type: {output_type}".format(output_type=output_type))


def play_by_play_to_csv(rows, output_file_path, write_option):
    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=play_by_play_fieldname)
        writer.writeheader()
        writer.writerows(
            {
                "quarter": row["quarter"],
                "timestamp": row["timestamp"],
                "side": row["side"],
                "away_score": row["away_score"],
                "home_score": row["home_score"],
                "description": row["description"]
            } for row in rows["plays"]
        )
