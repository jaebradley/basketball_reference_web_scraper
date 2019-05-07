from lxml import html

from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM, POSITION_ABBREVIATIONS_TO_POSITION
from basketball_reference_web_scraper.utilities import str_to_int


def parse_player_season_totals(row):
    return {
        "slug": str(row[1].get("data-append-csv")),
        "name": str(row[1].text_content()),
        "positions": parse_positions(row[2].text_content()),
        "age": str_to_int(row[3].text_content(), default=None),
        "team": TEAM_ABBREVIATIONS_TO_TEAM.get(row[4].text_content()),
        "games_played": str_to_int(row[5].text_content()),
        "games_started": str_to_int(row[6].text_content()),
        "minutes_played": str_to_int(row[7].text_content()),
        "made_field_goals": str_to_int(row[8].text_content()),
        "attempted_field_goals": str_to_int(row[9].text_content()),
        "made_three_point_field_goals": str_to_int(row[11].text_content()),
        "attempted_three_point_field_goals": str_to_int(row[12].text_content()),
        "made_free_throws": str_to_int(row[18].text_content()),
        "attempted_free_throws": str_to_int(row[19].text_content()),
        "offensive_rebounds": str_to_int(row[21].text_content()),
        "defensive_rebounds": str_to_int(row[22].text_content()),
        "assists": str_to_int(row[24].text_content()),
        "steals": str_to_int(row[25].text_content()),
        "blocks": str_to_int(row[26].text_content()),
        "turnovers": str_to_int(row[27].text_content()),
        "personal_fouls": str_to_int(row[28].text_content()),
    }


def parse_players_season_totals(page):
    tree = html.fromstring(page)
    # Basketball Reference includes individual rows for players that played for multiple teams in a season
    # These rows have a separate class ("italic_text partial_table") than the players that played for a single team
    # across a season.
    rows = tree.xpath('//table[@id="totals_stats"]/tbody/tr[contains(@class, "full_table") or contains(@class, "italic_text partial_table") and not(contains(@class, "rowSum"))]')
    totals = []
    for row in rows:
        # Basketball Reference includes a "total" row for players that got traded
        # which is essentially a sum of all player team rows
        # I want to avoid including those, so I check the "team" field value for "TOT"
        if row[4].text_content() != "TOT":
            totals.append(parse_player_season_totals(row))
    return totals


def parse_positions(positions_content):
    parsed_positions = list(
        map(
            lambda position_abbreviation: POSITION_ABBREVIATIONS_TO_POSITION.get(position_abbreviation),
            positions_content.split("-")
        )
    )
    return [position for position in parsed_positions if position is not None]
