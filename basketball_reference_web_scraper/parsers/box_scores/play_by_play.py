import re

from lxml import html

from basketball_reference_web_scraper.data import Location
from basketball_reference_web_scraper.data import Team

TIME_REGEX = "([0-9]+):([0-9]+)\.([0-9]+)"
SCORE_REGEX = "([0-9]+)-([0-9]+)"


def parse_time(time_str):
    time = re.search(TIME_REGEX, time_str.strip())
    if time:
        return float(time.group(1)) * 60 + float(time.group(2)) + float(time.group(3)) / 10
    else:
        return -1.0


def parse_play_by_plays(page, home_team):
    tree = html.fromstring(page.decode("utf-8", errors="replace"))
    table = tree.xpath('//table[@id="pbp"]')
    away_team = Team[tree.xpath("//*[@id=\"content\"]/div[2]/div[1]/div[1]/strong/a")[0]
        .text_content()
        .upper()
        .replace(" ", "_")]
    quarter = 0
    result = []
    for row in table[0][1:]:
        # quarters are partitioned by 6 column-spanned headers
        if row[0].get("colspan") == "6":
            quarter += 1
        # some rules to avoid trying to parse other clutter
        elif row[1].get("colspan") != "5" and row[0].get("aria-label") != "Time":
            result.append(parse_play_by_play(row, quarter, away_team, home_team))
    return result


def parse_play_by_play(row, quarter, away_team, home_team):
    score = re.search(SCORE_REGEX, row[3].text_content().strip())
    location = Location.HOME if row[1].text_content().strip() == "" else Location.AWAY
    return {
        "quarter": quarter,
        "timestamp": parse_time(row[0].text_content()),
        "side": location,
        "away_team": away_team,
        "home_team": home_team,
        "away_score": int(score.group(1)),
        "home_score": int(score.group(2)),
        "description": row[1].text_content().strip() if location == Location.AWAY else row[5].text_content().strip()
    }
