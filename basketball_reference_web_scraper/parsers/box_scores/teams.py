from lxml import html


def parse_team_total(team_total_footer):
    cells = team_total_footer.xpath('tr/td')
    return {
        "minutes_played": int(cells[0].text_content()),
        "made_field_goals": int(cells[1].text_content()),
        "attempted_field_goals": int(cells[2].text_content()),
        "made_three_point_field_goals": int(cells[4].text_content()),
        "attempted_three_point_field_goals": int(cells[5].text_content()),
        "made_free_throws": int(cells[7].text_content()),
        "attempted_free_throws": int(cells[8].text_content()),
        "offensive_rebounds": int(cells[10].text_content()),
        "defensive_rebounds": int(cells[11].text_content()),
        "assists": int(cells[13].text_content()),
        "steals": int(cells[14].text_content()),
        "blocks": int(cells[15].text_content()),
        "turnovers": int(cells[16].text_content()),
        "personal_fouls": int(cells[17].text_content()),
    }


def parse_team_totals(page):
    tree = html.fromstring(page)
    tables = tree.xpath('//table[contains(@class, "stats_table")]')
    team_totals = list()
    for table in tables:
        if "basic" in table.attrib["id"]:
            for footer in table.xpath("tfoot"):
                team_totals.append(footer)
    return list(map(lambda team_total: parse_team_total(team_total), team_totals))
