import urllib

from basketball_reference_web_scraper.http_service import HTTPService


class PlayByPlayURLSerializer:
    def __init__(self, year_serializer, month_serializer, day_serializer, team_abbreviation_serializer):
        self._year_serializer = year_serializer
        self._month_serializer = month_serializer
        self._day_serializer = day_serializer
        self._team_abbreviation_serializer = team_abbreviation_serializer

    def serialize(self, play_by_play_url: PlayByPlayURL) -> str:
        filename = f"{year}.html"
        # From https://docs.python.org/3.9/library/urllib.parse.html#urllib.parse.urlsplit
        parts = (
            "https",
            HTTPService.BASE_URL,
            urllib.parse.urljoin("boxscores", "pbp", filename)
        )
        return urllib.parse.urljoin(parts)
