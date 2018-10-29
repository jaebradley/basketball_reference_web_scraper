from lxml import html
import datetime
import pytz

from basketball_reference_web_scraper.data import Team

TEAM_NAME_TO_TEAM = {
    member.value: member
    for (_, member) in Team.__members__.items()
}

TEAM_NAME_TO_TEAM["NEW ORLEANS/OKLAHOMA CITY HORNETS"] = Team.NEW_ORLEANS_OKLAHOMA_CITY_HORNETS


def parse_start_time(formatted_date, formatted_time_of_day):
    if formatted_time_of_day is not None and formatted_time_of_day not in ["", " "]:
        # Starting in 2018, the start times had a "p" or "a" appended to the end
        # Between 2001 and 2017, the start times had a "pm" or "am"
        #
        # https://www.basketball-reference.com/leagues/NBA_2018_games.html
        # vs.
        # https://www.basketball-reference.com/leagues/NBA_2001_games.html
        is_prior_format = formatted_time_of_day[-2:] == "am" or formatted_time_of_day[-2:] == "pm"

        # If format contains only "p" or "a" add an "m" so it can be parsed by datetime module
        if is_prior_format:
            combined_formatted_time = formatted_date + " " + formatted_time_of_day
        else:
            combined_formatted_time = formatted_date + " " + formatted_time_of_day + "m"

        if is_prior_format:
            start_time = datetime.datetime.strptime(combined_formatted_time, "%a, %b %d, %Y %I:%M %p")
        else:
            start_time = datetime.datetime.strptime(combined_formatted_time, "%a, %b %d, %Y %I:%M%p")
    else:
        start_time = datetime.datetime.strptime(formatted_date, "%a, %b %d, %Y")

    # All basketball reference times seem to be in Eastern
    est = pytz.timezone("US/Eastern")
    localized_start_time = est.localize(start_time)
    return localized_start_time.astimezone(pytz.utc)


def parse_game(row):
    start_time = parse_start_time(formatted_date=row[0].text_content(), formatted_time_of_day=row[1].text_content())
    return {
        "start_time": start_time,
        "away_team": TEAM_NAME_TO_TEAM[row[2].text_content().upper()],
        "away_team_score": int(row[3].text_content()),
        "home_team": TEAM_NAME_TO_TEAM[row[4].text_content().upper()],
        "home_team_score": int(row[5].text_content()),
    }


def parse_schedule(page):
    tree = html.fromstring(page)
    rows = tree.xpath('//table[@id="schedule"]//tbody/tr')
    schedule = []
    for row in rows:
        if row.text_content() != "Playoffs":
            schedule.append(parse_game(row))
    return schedule


def parse_schedule_for_month_url_paths(page):
    tree = html.fromstring(page)
    months = tree.xpath('//div[@id="content"]/div[@class="filter"]/div[not(contains(@class, "current"))]/a')
    return list(map(lambda month: month.attrib['href'], months))
