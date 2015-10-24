import json

from basketball_reference_web_scraper.models.event import Event


class EventJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Event):
            return super(EventJsonEncoder, self).default(obj)

        return obj.__dict__
