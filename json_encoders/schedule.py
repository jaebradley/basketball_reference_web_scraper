import json

from basketball_reference_web_scraper.models.schedule import Schedule


class ScheduleJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Schedule):
            return super(ScheduleJsonEncoder, self).default(obj)

        return obj.__dict__
