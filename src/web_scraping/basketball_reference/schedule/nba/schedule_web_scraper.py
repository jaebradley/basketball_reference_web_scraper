from src.web_scraping.basketball_reference.schedule.nba.raw_events_returner import RawEventsReturner
from src.web_scraping.basketball_reference.schedule.nba.parsed_event_list_returner import ParsedEventListReturner
from src.persistence.model.schedule import Schedule
from src.persistence.json.encoders.schedule import ScheduleJsonEncoder
import json


class SeasonScheduleWebScraper:
    def __init__(self):
        pass

    @staticmethod
    def return_schedule(season_start_year):
        raw_events = RawEventsReturner.return_raw_events(season_start_year=season_start_year)
        parsed_event_list = ParsedEventListReturner.return_parsed_event_list(raw_html_events=raw_events)
        # TODO: change hard-coded end season_start_year value
        return Schedule(parsed_event_list, start_year=season_start_year, end_year=season_start_year + 1)

    @staticmethod
    def return_json_encoded_schedule(season_start_year):
        raw_events = RawEventsReturner.return_raw_events(season_start_year=season_start_year)
        parsed_event_list = ParsedEventListReturner.return_parsed_json_encoded_event_list(raw_html_events=raw_events)
        # TODO: change hard-coded end year value
        return json.dumps(Schedule(parsed_event_list, start_year=season_start_year, end_year=season_start_year + 1), cls=ScheduleJsonEncoder)