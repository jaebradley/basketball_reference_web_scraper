from datetime import datetime
from json import JSONEncoder


class ScheduleEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()

        return JSONEncoder.default(self, obj)

