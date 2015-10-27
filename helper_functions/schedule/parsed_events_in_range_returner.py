import datetime
import pytz
from basketball_reference_web_scraper.helper_functions.schedule.raw_events_returner import RawEventsHTMLReturner
from basketball_reference_web_scraper.helper_functions.schedule.parsed_raw_event_start_time_in_utc_returner import ParsedRawEventStartTimeInUtcReturner
from basketball_reference_web_scraper.helper_functions.schedule.parsed_event_list_returner import ParsedEventListReturner


class ParsedEventsInRangeReturner:
    def __init__(self):
        pass

    @staticmethod
    def return_scheduled_events_in_range_inclusive(utc_start_datetime, utc_end_datetime):

        assert isinstance(utc_start_datetime, datetime.datetime)
        assert isinstance(utc_end_datetime, datetime.datetime)
        assert utc_start_datetime.tzinfo == pytz.utc
        assert utc_end_datetime.tzinfo == pytz.utc

        assert utc_start_datetime <= utc_end_datetime

        candidate_events_year = utc_start_datetime.year - 1
        candidate_events_end_year = utc_end_datetime.year + 3
        all_events_in_range = False
        parsed_events_in_range = list()

        while not all_events_in_range and candidate_events_year <= candidate_events_end_year:
            raw_events_html = RawEventsHTMLReturner.return_raw_events_html(candidate_events_year)
            first_event_utc_start_time = ParsedRawEventStartTimeInUtcReturner.return_parsed_start_time_in_utc(
                raw_events_html[0:9][0].text_content(),
                raw_events_html[0:9][1].text_content()
            )

            last_event_utc_start_time = ParsedRawEventStartTimeInUtcReturner.return_parsed_start_time_in_utc(
                raw_events_html[raw_events_html.__len__() - 9: raw_events_html.__len__() - 1][0].text_content(),
                raw_events_html[raw_events_html.__len__() - 9: raw_events_html.__len__() - 1][1].text_content(),
            )

            # start time and end time are in season
            if first_event_utc_start_time <= utc_start_datetime and last_event_utc_start_time >= utc_end_datetime:
                parsed_events_in_range.extend(ParsedEventListReturner.return_parsed_event_list_in_range(raw_events_html, utc_start_datetime, utc_end_datetime))
                all_events_in_range = True

            # start time is in season and end time is not
            elif first_event_utc_start_time <= utc_start_datetime and last_event_utc_start_time < utc_end_datetime:
                parsed_events_in_range.extend(ParsedEventListReturner.return_parsed_event_list_in_range(raw_events_html, utc_start_datetime, utc_end_datetime))
                candidate_events_year += 1

            # start time is not in season and end time is
            elif first_event_utc_start_time > utc_start_datetime and last_event_utc_start_time >= utc_end_datetime:
                parsed_events_in_range.extend(ParsedEventListReturner.return_parsed_event_list_in_range(raw_events_html, utc_start_datetime, utc_end_datetime))
                all_events_in_range = True

            # start time is less than season start and end time is greater than season start
            elif first_event_utc_start_time >= utc_start_datetime and last_event_utc_start_time < utc_end_datetime:
                parsed_events_in_range.extend(ParsedEventListReturner.return_parsed_event_list_in_range(raw_events_html, utc_start_datetime, utc_end_datetime))
                candidate_events_year += 1

            # neither start time greater than season
            elif last_event_utc_start_time < utc_start_datetime:
                candidate_events_year += 1

            # end time less than season
            elif first_event_utc_start_time > utc_end_datetime:
                all_events_in_range = True

            else:
                raise RuntimeError("unexpected {0} - {1}".format(first_event_utc_start_time, last_event_utc_start_time))

        return parsed_events_in_range

    @staticmethod
    def return_json_encoded_scheduled_events_in_range_inclusive(utc_start_datetime, utc_end_datetime):

        assert isinstance(utc_start_datetime, datetime.datetime)
        assert isinstance(utc_end_datetime, datetime.datetime)
        assert utc_start_datetime.tzinfo == pytz.utc
        assert utc_end_datetime.tzinfo == pytz.utc

        assert utc_start_datetime <= utc_end_datetime

        candidate_events_year = utc_start_datetime.year - 1
        candidate_events_end_year = utc_end_datetime.year + 3
        all_events_in_range = False
        parsed_events_in_range = list()

        while not all_events_in_range and candidate_events_year <= candidate_events_end_year:
            raw_events_html = RawEventsHTMLReturner.return_raw_events_html(candidate_events_year)
            first_event_utc_start_time = ParsedRawEventStartTimeInUtcReturner.return_parsed_start_time_in_utc(
                raw_events_html[0:9][0].text_content(),
                raw_events_html[0:9][1].text_content()
            )

            last_event_utc_start_time = ParsedRawEventStartTimeInUtcReturner.return_parsed_start_time_in_utc(
                raw_events_html[raw_events_html.__len__() - 9: raw_events_html.__len__() - 1][0].text_content(),
                raw_events_html[raw_events_html.__len__() - 9: raw_events_html.__len__() - 1][1].text_content(),
            )

            # start time and end time are in season
            if first_event_utc_start_time <= utc_start_datetime and last_event_utc_start_time >= utc_end_datetime:
                parsed_events_in_range.extend(ParsedEventListReturner.return_parsed_json_encoded_event_list_in_range(raw_events_html, utc_start_datetime, utc_end_datetime))
                all_events_in_range = True

            # start time is in season and end time is not
            elif first_event_utc_start_time <= utc_start_datetime and last_event_utc_start_time < utc_end_datetime:
                parsed_events_in_range.extend(ParsedEventListReturner.return_parsed_json_encoded_event_list_in_range(raw_events_html, utc_start_datetime, utc_end_datetime))
                candidate_events_year += 1

            # start time is not in season and end time is
            elif first_event_utc_start_time > utc_start_datetime and last_event_utc_start_time >= utc_end_datetime:
                parsed_events_in_range.extend(ParsedEventListReturner.return_parsed_json_encoded_event_list_in_range(raw_events_html, utc_start_datetime, utc_end_datetime))
                all_events_in_range = True

            # start time is less than season start and end time is greater than season start
            elif first_event_utc_start_time >= utc_start_datetime and last_event_utc_start_time < utc_end_datetime:
                parsed_events_in_range.extend(ParsedEventListReturner.return_parsed_json_encoded_event_list_in_range(raw_events_html, utc_start_datetime, utc_end_datetime))
                candidate_events_year += 1

            # neither start time greater than season
            elif last_event_utc_start_time < utc_start_datetime:
                candidate_events_year += 1

            # end time less than season
            elif first_event_utc_start_time > utc_end_datetime:
                all_events_in_range = True

            else:
                raise RuntimeError("unexpected {0} - {1}".format(first_event_utc_start_time, last_event_utc_start_time))

        return parsed_events_in_range