import os.path

from basketball_reference_web_scraper.parsers import PositionAbbreviationParser
from basketball_reference_web_scraper.team_season.html import TeamSeasonPage


class PlayerUrlSlugParser:

    """
    URLs look like "/players/b/bantoda01.html"
    """
    def parse(self, url: str) -> str:
        (head, tail) = os.path.split(url)
        if tail is None:
            raise ValueError(f"{url} is unparseable")

        if not tail.endswith(".html"):
            raise ValueError(f"{url} does not end with .html")

        return tail.removesuffix(".html")


class RosterParser:
    def __init__(self, slug_parser: PlayerUrlSlugParser, position_abbreviation_parser: PositionAbbreviationParser):
        self.slug_parser = slug_parser
        self.position_abbreviation_parser = position_abbreviation_parser

    def parse(self, team_season_page: TeamSeasonPage):
        return [{
            "slug": self.slug_parser.parse(row.player_url),
            "name": row.name,
            # A player's number can be "00".
            # A player that is injured will not have a number.
            "number": row.number if row.number else None,
            "position": self.position_abbreviation_parser.from_abbreviation(row.position_abbreviation),
        } for row in team_season_page.roster_rows]

