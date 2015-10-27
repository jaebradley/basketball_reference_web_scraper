import json

from basketball_reference_web_scraper.models.event import Event
from basketball_reference_web_scraper.helper_functions.schedule.parsed_raw_event_start_time_in_utc_returner import ParsedRawEventStartTimeInUtcReturner
from basketball_reference_web_scraper.json_encoders.event import EventJsonEncoder


class ParsedEventListReturner:
    def __init__(self):
        pass

    @staticmethod
    def return_parsed_event_list(raw_html_events):
        event_list = list()
        # TODO: fix hard-coded length
        for counter in range(0, raw_html_events.__len__(), 9):
            event_information = raw_html_events[counter:counter + 9]
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

    @staticmethod
    def return_parsed_json_encoded_event_list(raw_html_events):
        json_encoded_event_list = list()
        # TODO: fix hard-coded length
        for counter in range(0, raw_html_events.__len__(), 9):
            event_information = raw_html_events[counter:counter + 9]
            utc_start_time = ParsedRawEventStartTimeInUtcReturner.return_parsed_start_time_in_utc(
                event_information[0].text_content(),
                event_information[1].text_content()
            )
            event = Event(
                str(utc_start_time),
                event_information[3].text_content(),
                event_information[5].text_content()
            )
            json_encoded_event_list.append(json.dumps(event, cls=EventJsonEncoder))
        return json_encoded_event_list

    @staticmethod
    def return_parsed_event_list_in_range(raw_html_events, start_datetime, end_datetime):
        event_list = list()
        for counter in range(0, raw_html_events.__len__(), 9):
            event_information = raw_html_events[counter:counter + 9]
            utc_start_time = ParsedRawEventStartTimeInUtcReturner.return_parsed_start_time_in_utc(
                event_information[0].text_content(),
                event_information[1].text_content()
            )
            if utc_start_time >= start_datetime and utc_start_time <= end_datetime:
                event = Event(
                    utc_start_time,
                    event_information[3].text_content(),
                    event_information[5].text_content()
                )
                event_list.append(event)
        return event_list

    @staticmethod
    def return_parsed_json_encoded_event_list_in_range(raw_html_events, start_datetime, end_datetime):
        json_encoded_event_list = list()
        for counter in range(0, raw_html_events.__len__(), 9):
            event_information = raw_html_events[counter:counter + 9]
            utc_start_time = ParsedRawEventStartTimeInUtcReturner.return_parsed_start_time_in_utc(
                event_information[0].text_content(),
                event_information[1].text_content()
            )
            if utc_start_time >= start_datetime and utc_start_time <= end_datetime:
                event = Event(
                    str(utc_start_time),
                    event_information[3].text_content(),
                    event_information[5].text_content()
                )
                json_encoded_event_list.append(json.dumps(event, cls=EventJsonEncoder))
        return json_encoded_event_list