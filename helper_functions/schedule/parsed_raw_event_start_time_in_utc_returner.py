import datetime
import pytz


class ParsedRawEventStartTimeInUtcReturner:
    def __init__(self):
        pass

    @staticmethod
    def return_parsed_start_time_in_utc(raw_event_date, raw_event_hour_of_day):
        if raw_event_hour_of_day is not None and raw_event_hour_of_day not in ["", " "]:
            parsed_event_start_time = datetime.datetime.strptime(raw_event_date + raw_event_hour_of_day, "%a, %b %d, %Y%I:%M %p")
        else:
            parsed_event_start_time = datetime.datetime.strptime(raw_event_date, "%a, %b %d, %Y")
        est = pytz.timezone("US/Eastern")
        parsed_est_start_time = est.localize(parsed_event_start_time)
        return parsed_est_start_time.astimezone(pytz.utc)
