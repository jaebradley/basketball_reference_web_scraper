import json

from json_encoders.schedule import Schedule


class ScheduleJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Schedule):
            return super(ScheduleJsonEncoder, self).default(obj)

        return obj.__dict__
