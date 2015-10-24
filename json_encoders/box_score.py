import json

from models.box_score import BoxScore


class BoxScoreJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, BoxScore):
            return super(BoxScoreJsonEncoder, self).default(obj)

        return obj.__dict__