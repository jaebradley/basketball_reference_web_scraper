from src.web_scraping.basketball_reference.schedule.nba.raw_events_returner import RawEventsReturner
from src.web_scraping.basketball_reference.schedule.nba.parsed_event_list_returner import ParsedEventListReturner
from src.persistence.model.schedule import Schedule


class ScheduleWebScraper:
    def __init__(self):
        pass

    @staticmethod
    def return_event_list(year):
        raw_events = RawEventsReturner.return_raw_events(year=year)
        parsed_event_list = ParsedEventListReturner.return_parsed_event_list(raw_html_events=raw_events)
        # TODO: change hard-coded end year value
        return Schedule(parsed_event_list, start_year=year, end_year=year + 1)
