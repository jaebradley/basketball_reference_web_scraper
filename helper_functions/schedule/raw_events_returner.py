import urllib2

from lxml import html

from helper_functions.schedule.schedule_url_generator import ScheduleUrlGenerator


class RawEventsReturner:
    def __init__(self):
        pass

    @staticmethod
    def return_raw_events(season_start_year):
        raw_content = urllib2.urlopen(ScheduleUrlGenerator.generate_url(season_start_year + 1)).read()
        schedule_html = html.fromstring(raw_content)
        raw_html_events = schedule_html.xpath('//div[@id="div_games"]//td')
        return raw_html_events