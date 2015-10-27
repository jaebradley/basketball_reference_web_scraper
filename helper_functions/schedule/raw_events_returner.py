import urllib2

from lxml import html

from basketball_reference_web_scraper.helper_functions.schedule.season_schedule_url_generator import SeasonScheduleUrlGenerator


class RawEventsHTMLReturner:
    def __init__(self):
        pass

    @staticmethod
    def return_raw_events_html(season_start_year):
        raw_content = urllib2.urlopen(SeasonScheduleUrlGenerator.generate_url(season_start_year + 1)).read()
        schedule_html = html.fromstring(raw_content)
        raw_html_events = schedule_html.xpath('//div[@id="div_games"]//td')
        return raw_html_events