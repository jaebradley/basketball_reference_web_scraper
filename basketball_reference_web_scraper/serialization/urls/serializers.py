from datetime import date
from urllib.parse import urljoin, SplitResult

from basketball_reference_web_scraper.data import TeamAbbreviation
from basketball_reference_web_scraper.serialization.urls.models import PlayByPlayURLData


# TODO: @jaebradley once Python 3.7 support is deprecated, add a Serializer Protocol
class DateSerializer:
    def serialize(self, value: date) -> str:
        return value.strftime("%Y%m%d")


class TeamAbbreviationSerializer:
    def serialize(self, value: TeamAbbreviation) -> str:
        return value.name


class PlayByPlayURLSerializer:
    def __init__(self, date_serializer, team_abbreviation_serializer):
        self._date_serializer = date_serializer
        self._team_abbreviation_serializer = team_abbreviation_serializer

    def serialize(self, value: PlayByPlayURLData) -> str:
        # From https://docs.python.org/3.9/library/urllib.parse.html#urllib.parse.urlsplit
        return SplitResult(
            scheme="https",
            netloc="www.basketball-reference.com",
            path=urljoin(
                "/boxscores/",
                urljoin(
                    "pbp/",
                    f"{self._date_serializer.serialize(value.date)}0{self._team_abbreviation_serializer.serialize(value.team_abbreviation)}.html")),
            query="",
            fragment=""
        ).geturl()


# TODO: @jaebradley create a proper singleton metaclass
DEFAULT_PLAY_BY_PLAY_URL_SERIALIZER = PlayByPlayURLSerializer(
    date_serializer=DateSerializer(),
    team_abbreviation_serializer=TeamAbbreviationSerializer()
)
