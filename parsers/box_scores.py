import time
import datetime
from lxml import html

from data import Location, Outcome


def parse_location(symbol):
    if symbol == "@":
        return Location.AWAY
    return Location.HOME


def parse_outcome(symbol):
    if symbol == "W":
        return Outcome.WIN
    elif symbol == "L":
        return Outcome.LOSS
    raise ValueError("Unknown symbol: {symbol}".format(symbol=symbol))


def parse_seconds_played(formatted_playing_time):
    if formatted_playing_time == "":
        return 0

    parsed_time = time.strptime(formatted_playing_time, "%M:%S")
    return datetime.timedelta(
        hours=parsed_time.tm_hour,
        minutes=parsed_time.tm_min,
        seconds=parsed_time.tm_sec,
    ).total_seconds()


def parse_player_box_score(row):
    return {
        "name": str(row[1].text_content()),
        "team": row[2].text_content(),
        "location": parse_location(row[3].text_content()),
        "opponent": row[4].text_content(),
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


def parse_box_score(page):
    tree = html.fromstring(page)
    rows = tree.xpath('//table[@id="stats"]//tbody/tr[not(contains(@class, "thead"))]')
    return list(map(lambda row: parse_player_box_score(row), rows))
