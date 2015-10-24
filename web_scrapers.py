import json

from helper_functions.schedule.raw_events_returner import RawEventsReturner
from helper_functions.schedule.parsed_event_list_returner import ParsedEventListReturner
from models.schedule import Schedule
from json_encoders.schedule import ScheduleJsonEncoder

from helper_functions.box_score.box_score_url_generator import BoxScoreUrlGenerator
from helper_functions.box_score.box_scores_html_returner import BoxScoresHtmlReturner
from helper_functions.box_score.parsed_box_scores_returner import ParsedBoxScoresReturner
import datetime


def return_schedule(season_start_year):
    raw_events = RawEventsReturner.return_raw_events(season_start_year=season_start_year)
    parsed_event_list = ParsedEventListReturner.return_parsed_event_list(raw_html_events=raw_events)
    # TODO: change hard-coded end season_start_year value
    return Schedule(parsed_event_list, start_year=season_start_year, end_year=season_start_year + 1)


def return_json_encoded_schedule(season_start_year):
    raw_events = RawEventsReturner.return_raw_events(season_start_year=season_start_year)
    parsed_event_list = ParsedEventListReturner.return_parsed_json_encoded_event_list(raw_html_events=raw_events)
    # TODO: change hard-coded end year value
    return json.dumps(Schedule(parsed_event_list, start_year=season_start_year, end_year=season_start_year + 1), cls=ScheduleJsonEncoder)


def return_box_scores_for_date(date):
    generated_url = BoxScoreUrlGenerator.generate_url(date=date)
    raw_box_scores_html = BoxScoresHtmlReturner.return_html(box_score_url=generated_url)
    box_scores = ParsedBoxScoresReturner.return_box_scores(box_scores_html=raw_box_scores_html, date=date)
    return box_scores


def return_json_encoded_box_scores_for_date(date):
    generated_url = BoxScoreUrlGenerator.generate_url(date=date)
    raw_box_scores_html = BoxScoresHtmlReturner.return_html(box_score_url=generated_url)
    json_encoded_box_scores = ParsedBoxScoresReturner.return_json_encoded_box_scores(box_scores_html=raw_box_scores_html, date=date)
    return json_encoded_box_scores