from datetime import datetime
from json import JSONEncoder
from enum import Enum


class BasketballReferenceJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()

        if isinstance(obj, Enum):
            return obj.value

        return JSONEncoder.default(self, obj)

