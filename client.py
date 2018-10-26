import json

from http_client import get_box_scores
from data import OutputType
from errors import UnknownOutputType


def box_scores(day, month, year, output_type=None):
    values = get_box_scores(day=day, month=month, year=year)
    if output_type is None:
        return values

    if output_type == OutputType.JSON:
        return json.dumps(values, sort_keys=True, indent=4)

    raise UnknownOutputType(output_type)