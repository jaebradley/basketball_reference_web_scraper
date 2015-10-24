import json

from json_encoders.event import Event


class EventJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Event):
            return super(EventJsonEncoder, self).default(obj)

        return obj.__dict__
