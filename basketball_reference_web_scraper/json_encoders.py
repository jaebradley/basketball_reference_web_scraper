from datetime import datetime
from enum import Enum
from json import JSONEncoder


class BasketballReferenceJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()

        if isinstance(obj, Enum):
            return obj.value

        return JSONEncoder.default(self, obj)

