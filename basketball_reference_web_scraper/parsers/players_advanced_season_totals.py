from lxml import html

from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM
from basketball_reference_web_scraper.parsers.positions import parse_positions
from basketball_reference_web_scraper.utilities import str_to_int, str_to_float


def parse_player_advanced_season_total(row):
    return {
        "slug": str(row[1].get("data-append-csv")),
        "name": str(row[1].text_content()),
        "positions": parse_positions(row[2].text_content()),
        "age": str_to_int(row[3].text_content(), default=None),
        "team": TEAM_ABBREVIATIONS_TO_TEAM.get(row[4].text_content()),
        "games_played": str_to_int(row[5].text_content()),
        "minutes_played": str_to_int(row[6].text_content()),
        "player_efficiency_rating": str_to_float(row[7].text_content()),
        "true_shooting_percentage": str_to_float(row[8].text_content()),
        "three_point_attempt_rate": str_to_float(row[9].text_content()),
        "free_throw_attempt_rate": str_to_float(row[10].text_content()),
        "offensive_rebound_percentage": str_to_float(row[11].text_content()),
        "defensive_rebound_percentage": str_to_float(row[12].text_content()),
        "total_rebound_percentage": str_to_float(row[13].text_content()),
        "assist_percentage": str_to_float(row[14].text_content()),
        "steal_percentage": str_to_float(row[15].text_content()),
        "block_percentage": str_to_float(row[16].text_content()),
        "turnover_percentage": str_to_float(row[17].text_content()),
        "usage_percentage": str_to_float(row[18].text_content()),
        "offensive_win_shares": str_to_float(row[20].text_content()),
        "defensive_win_shares": str_to_float(row[21].text_content()),
        "win_shares": str_to_float(row[22].text_content()),
        "win_shares_per_48_minutes": str_to_float(row[23].text_content()),
        "offensive_box_plus_minus": str_to_float(row[25].text_content()),
        "defensive_box_plus_minus": str_to_float(row[26].text_content()),
        "box_plus_minus": str_to_float(row[27].text_content()),
        "value_over_replacement_player": str_to_float(row[28].text_content()),
    }


def parse_players_advanced_season_totals(page):
    tree = html.fromstring(page)

    rows = tree.xpath('//table[@id="advanced_stats"]/tbody/tr[contains(@class, "full_table") or contains(@class, "italic_text partial_table") and not(contains(@class, "rowSum"))]')
    advanced = []
    for row in rows:
        # Basketball Reference includes a "total" row for players that got traded
        # which is essentially a sum of all player team rows
        # I want to avoid including those, so I check the "team" field value for "TOT"
        if row[4].text_content() != "TOT":
            advanced.append(parse_player_advanced_season_total(row))
    return advanced
