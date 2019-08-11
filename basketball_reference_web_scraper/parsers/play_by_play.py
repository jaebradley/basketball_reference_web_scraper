import re
from datetime import datetime

from lxml import html

from basketball_reference_web_scraper.data import Team, PeriodType

TIMESTAMP_FORMAT = "%M:%S.%f"
SCORE_REGEX = "([0-9]+)-([0-9]+)"


def parse_period_details(period_count):
    if period_count > 4:
        return {
            "period": period_count - 4,
            "type": PeriodType.OVERTIME,
        }

    return {
        "period": period_count,
        "type": PeriodType.QUARTER
    }


def parse_timestamp(time_stamp):
    dt = datetime.strptime(time_stamp, TIMESTAMP_FORMAT)
    return float((dt.minute * 60) + dt.second + (dt.microsecond / 1000000))


def parse_play_by_plays(page, home_team):
    tree = html.fromstring(page.decode("utf-8", errors="replace"))
    table = tree.xpath('//table[@id="pbp"]')
    away_team = Team[tree.xpath("//*[@id=\"content\"]/div[2]/div[1]/div[1]/strong/a")[0]
        .text_content()
        .upper()
        .replace(" ", "_")]
    period_count = 0
    result = []
    for row in table[0][1:]:
        # quarters are partitioned by 6 column-spanned headers
        if row[0].get("colspan") == "6":
            period_count += 1
        # some rules to avoid trying to parse other clutter
        elif row[1].get("colspan") != "5" and row[0].get("aria-label") != "Time":
            result.append(parse_play_by_play(row, period_count, away_team, home_team))
    return result


def parse_play_by_play(row, period_count, away_team, home_team):
    period_details = parse_period_details(period_count)

    timestamp_value = row[0].text_content().strip()
    remaining_seconds_in_period = parse_timestamp(timestamp_value)

    combined_score_value = row[3].text_content().strip()
    parsed_scores = re.search(SCORE_REGEX, combined_score_value)

    away_team_play_description = row[1].text_content().strip()
    home_team_play_description = row[5].text_content().strip()

    if away_team_play_description != "":
        relevant_team = away_team
        description = away_team_play_description
    else:
        relevant_team = home_team
        description = home_team_play_description

    return {
        "period": period_details["period"],
        "period_type": period_details["type"],
        "remaining_seconds_in_period": remaining_seconds_in_period,
        "relevant_team": relevant_team,
        "away_team": away_team,
        "home_team": home_team,
        "away_score": int(parsed_scores.group(1)),
        "home_score": int(parsed_scores.group(2)),
        "description": description,
    }
