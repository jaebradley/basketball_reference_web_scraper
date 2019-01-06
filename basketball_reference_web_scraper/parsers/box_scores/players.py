from lxml import html

from basketball_reference_web_scraper.data import Location, Outcome, TEAM_ABBREVIATIONS_TO_TEAM


def parse_location(symbol):
    if symbol == "@":
        return Location.AWAY
    elif symbol == "":
        return Location.HOME
    raise ValueError("Unknown symbol: {symbol}".format(symbol=symbol))


def parse_outcome(symbol):
    if symbol == "W":
        return Outcome.WIN
    elif symbol == "L":
        return Outcome.LOSS
    raise ValueError("Unknown symbol: {symbol}".format(symbol=symbol))


def parse_seconds_played(formatted_playing_time):
    if formatted_playing_time == "":
        return 0

    # It seems like basketball reference formats everything in MM:SS
    # even when the playing time is greater than 59 minutes, 59 seconds.
    #
    # Because of this, we can't use strptime / %M as valid values are 0-59.
    # So have to parse time by splitting on ":" and assuming that
    # the first part is the minute part and the second part is the seconds part
    time_parts = formatted_playing_time.split(":")
    minutes_played = time_parts[0]
    seconds_played = time_parts[1]
    return 60 * int(minutes_played) + int(seconds_played)


def parse_player_box_score(row):
    return {
        "name": str(row[1].text_content()),
        "team": TEAM_ABBREVIATIONS_TO_TEAM[row[2].text_content()],
        "location": parse_location(row[3].text_content()),
        "opponent": TEAM_ABBREVIATIONS_TO_TEAM[row[4].text_content()],
        "outcome": parse_outcome(row[5].text_content()),
        "seconds_played": int(parse_seconds_played(row[6].text_content())),
        "made_field_goals": int(row[7].text_content()),
        "attempted_field_goals": int(row[8].text_content()),
        "made_three_point_field_goals": int(row[10].text_content()),
        "attempted_three_point_field_goals": int(row[11].text_content()),
        "made_free_throws": int(row[13].text_content()),
        "attempted_free_throws": int(row[14].text_content()),
        "offensive_rebounds": int(row[16].text_content()),
        "defensive_rebounds": int(row[17].text_content()),
        "assists": int(row[19].text_content()),
        "steals": int(row[20].text_content()),
        "blocks": int(row[21].text_content()),
        "turnovers": int(row[22].text_content()),
        "personal_fouls": int(row[23].text_content()),
        "game_score": float(row[25].text_content()),
    }


def parse_player_box_scores(page):
    tree = html.fromstring(page)
    rows = tree.xpath('//table[@id="stats"]//tbody/tr[not(contains(@class, "thead"))]')
    return list(map(lambda row: parse_player_box_score(row), rows))
