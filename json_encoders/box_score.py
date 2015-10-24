import json

from basketball_reference_web_scraper.models.box_score import BoxScore


class BoxScoreJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, BoxScore):
            return super(BoxScoreJsonEncoder, self).default(obj)

        return obj.__dict__