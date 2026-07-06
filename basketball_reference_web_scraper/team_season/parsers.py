import os.path

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
    def __init__(self, slug_parser: PlayerUrlSlugParser):
        self.slug_parser = slug_parser

    def parse(self, team_season_page: TeamSeasonPage):
        return [{
            "slug": self.slug_parser.parse(row.player_url),
            "name": row.name,
        } for row in team_season_page.roster_rows]

