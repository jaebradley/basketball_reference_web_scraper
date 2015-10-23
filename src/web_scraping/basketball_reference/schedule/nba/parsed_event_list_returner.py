from src.persistence.model.event import Event
from src.web_scraping.basketball_reference.schedule.nba.parsed_raw_event_start_time_in_utc_returner import ParsedRawEventStartTimeInUtcReturner
import time


class ParsedEventListReturner:
    def __init__(self):
        pass

    @staticmethod
    def return_parsed_event_list(raw_events):
        event_list = list()
        for counter in range(0, raw_events.__len__(), 9):
            event_information = raw_events[counter:counter + 9]
            utc_start_time = ParsedRawEventStartTimeInUtcReturner.return_parsed_start_time_in_utc(
                event_information[0].text_content(),
                event_information[1].text_content()
            )
            event = Event(
                utc_start_time,
                event_information[3].text_content(),
                event_information[5].text_content()
            )
            event_list.append(event)
        return event_list