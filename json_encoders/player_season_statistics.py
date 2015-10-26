import json

from basketball_reference_web_scraper.models.player_season_statistics import PlayerSeasonStatistics


class PlayerSeasonStatisticsJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, PlayerSeasonStatistics):
            return super(PlayerSeasonStatisticsJsonEncoder, self).default(obj)

        return obj.__dict__

