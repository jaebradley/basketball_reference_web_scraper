from datetime import datetime, date
from enum import Enum
from json import JSONEncoder


class FieldFormatter:
    @staticmethod
    def can_format(data):
        raise NotImplementedError()

    def __init__(self, data):
        self.data = data

    def format(self):
        raise NotImplementedError


class EnumFormatter(FieldFormatter):
    @staticmethod
    def can_format(data):
        return isinstance(data, Enum)

    def format(self):
        return self.data.value


class ListFormatter(FieldFormatter):
    @staticmethod
    def can_format(data):
        return isinstance(data, list)

    def format(self):
        return "-".join(map(lambda value: format_value(value=value), self.data))


class SetFormatter(FieldFormatter):
    @staticmethod
    def can_format(data):
        return isinstance(data, set)

    def format(self):
        return ListFormatter(data=list(self.data)).format()


FORMATTER_CLASSES = [
    EnumFormatter,
    ListFormatter,
    SetFormatter,
]


def format_value(value):
    formatter_class = next(
        (formatter_class for formatter_class in FORMATTER_CLASSES if formatter_class.can_format(value)),
        None,
    )

    if formatter_class is None:
        return value

    return formatter_class(data=value).format()


class BasketballReferenceJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()

        if isinstance(obj, Enum):
            return obj.value

        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)
