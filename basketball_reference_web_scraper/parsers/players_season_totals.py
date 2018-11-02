from lxml import html

from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM, POSITION_ABBREVIATIONS_TO_POSITION


def parse_player_season_totals(row):
    return {
        "name": str(row[1].text_content()),
        "position": POSITION_ABBREVIATIONS_TO_POSITION[row[2].text_content()],
        "age": int(row[3].text_content()),
        "team": TEAM_ABBREVIATIONS_TO_TEAM[row[4].text_content()],
        "games_played": int(row[5].text_content()),
        "games_started": int(row[6].text_content()),
        "minutes_played": int(row[7].text_content()),
        "made_field_goals": int(row[8].text_content()),
        "attempted_field_goals": int(row[9].text_content()),
        "made_three_point_field_goals": int(row[11].text_content()),
        "attempted_three_point_field_goals": int(row[12].text_content()),
        "made_free_throws": int(row[18].text_content()),
        "attempted_free_throws": int(row[19].text_content()),
        "offensive_rebounds": int(row[21].text_content()),
        "defensive_rebounds": int(row[22].text_content()),
        "assists": int(row[24].text_content()),
        "steals": int(row[25].text_content()),
        "blocks": int(row[26].text_content()),
        "turnovers": int(row[27].text_content()),
        "personal_fouls": int(row[28].text_content()),
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
