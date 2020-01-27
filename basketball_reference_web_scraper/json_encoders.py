from datetime import datetime, date
from enum import Enum
from json import JSONEncoder


class BasketballReferenceJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()

        if isinstance(obj, Enum):
            return obj.value

        return JSONEncoder.default(self, obj)

