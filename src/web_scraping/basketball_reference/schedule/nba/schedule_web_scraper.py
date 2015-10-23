from src.web_scraping.basketball_reference.schedule.nba.raw_events_returner import RawEventsReturner
from src.web_scraping.basketball_reference.schedule.nba.parsed_event_list_returner import ParsedEventListReturner


class ScheduleWebScraper:
    def __init__(self):
        pass

    @staticmethod
    def return_event_list(year):
        raw_events = RawEventsReturner.return_raw_events(year=year)
        parsed_event_list = ParsedEventListReturner.return_parsed_event_list(raw_events=raw_events)
        return parsed_event_list
