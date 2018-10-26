import json

from http_client import get_box_scores
from data import OutputType
from errors import UnknownOutputType
from output.box_scores import to_csv


def box_scores(day, month, year, output_type=None, relative_file_path=None):
    values = get_box_scores(day=day, month=month, year=year)
    if output_type is None:
        return values

    if output_type == OutputType.JSON:
        return json.dumps(values, sort_keys=True, indent=4)
    if output_type == OutputType.CSV:
        if relative_file_path is not None:
            return to_csv(relative_file_path=relative_file_path, box_scores=values)
        else:
            raise ValueError("CSV output must contain a file path")

    raise UnknownOutputType(output_type)