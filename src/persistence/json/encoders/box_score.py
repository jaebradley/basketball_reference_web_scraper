from src.persistence.model.box_score import BoxScore
import json


class BoxScoreJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, BoxScore):
            return super(BoxScoreJsonEncoder, self).default(obj)

        return obj.__dict__