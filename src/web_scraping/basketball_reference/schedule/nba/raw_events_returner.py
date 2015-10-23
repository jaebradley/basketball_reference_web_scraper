import urllib2

from lxml import html

from src.web_scraping.basketball_reference.schedule.nba.schedule_url_generator import ScheduleUrlGenerator


class RawEventsReturner:
    def __init__(self):
        pass

    @staticmethod
    def return_raw_events(year):
        raw_content = urllib2.urlopen(ScheduleUrlGenerator.generate_url(year)).read()
        schedule_html = html.fromstring(raw_content)
        raw_html_events = schedule_html.xpath('//td')
        return raw_html_events