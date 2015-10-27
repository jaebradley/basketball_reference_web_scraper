import json

from basketball_reference_web_scraper.helper_functions.schedule.raw_events_returner import RawEventsReturner
from basketball_reference_web_scraper.helper_functions.schedule.parsed_event_list_returner import ParsedEventListReturner
from basketball_reference_web_scraper.models.schedule import Schedule
from basketball_reference_web_scraper.json_encoders.schedule import ScheduleJsonEncoder

from basketball_reference_web_scraper.helper_functions.box_score.box_score_url_generator import BoxScoreUrlGenerator
from basketball_reference_web_scraper.helper_functions.box_score.box_scores_html_returner import BoxScoresHtmlReturner
from basketball_reference_web_scraper.helper_functions.box_score.parsed_box_scores_returner import ParsedBoxScoresReturner
from basketball_reference_web_scraper.helper_functions.player_season_statistics.player_season_statistics_url_generator import PlayerSeasonStatisticsUrlGenerator
from basketball_reference_web_scraper.helper_functions.player_season_statistics.player_season_statistics_html_returner import PlayerSeasonStatisticsHtmlReturner
from basketball_reference_web_scraper.helper_functions.player_season_statistics.parsed_player_season_statistics_returner import ParsedPlayerSeasonStatisticsReturner


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


def return_all_player_season_statistics(season_start_year):
    generated_url = PlayerSeasonStatisticsUrlGenerator.generate_url(season_start_year=season_start_year)
    raw_player_season_statistics_html = PlayerSeasonStatisticsHtmlReturner.return_html(player_season_statistics_url=generated_url)
    player_season_statistics = ParsedPlayerSeasonStatisticsReturner.return_all_player_season_statistics(raw_player_season_statistics_html, season_start_year)
    return player_season_statistics


def return_json_encoded_all_player_season_statistics(season_start_year):
    generated_url = PlayerSeasonStatisticsUrlGenerator.generate_url(season_start_year=season_start_year)
    raw_player_season_statistics_html = PlayerSeasonStatisticsHtmlReturner.return_html(player_season_statistics_url=generated_url)
    player_season_statistics = ParsedPlayerSeasonStatisticsReturner.return_json_encoded_all_player_season_statistics(raw_player_season_statistics_html, season_start_year)
    return player_season_statistics


def return_player_season_team_statistics(player_first_name, player_last_name, season_start_year, team_abbreviation):
    generated_url = PlayerSeasonStatisticsUrlGenerator.generate_url(season_start_year=season_start_year)
    raw_player_season_statistics_html = PlayerSeasonStatisticsHtmlReturner.return_html(player_season_statistics_url=generated_url)
    player_season_team_statistics = ParsedPlayerSeasonStatisticsReturner.return_player_season_team_statistics(raw_player_season_statistics_html, player_first_name, player_last_name, season_start_year, team_abbreviation)
    return player_season_team_statistics


def return_json_encoded_player_season_team_statistics(player_first_name, player_last_name, season_start_year, team_abbreviation):
    generated_url = PlayerSeasonStatisticsUrlGenerator.generate_url(season_start_year=season_start_year)
    raw_player_season_statistics_html = PlayerSeasonStatisticsHtmlReturner.return_html(player_season_statistics_url=generated_url)
    json_encoded_player_season_team_statistics = ParsedPlayerSeasonStatisticsReturner.return_json_encoded_player_season_team_statistics(raw_player_season_statistics_html, player_first_name, player_last_name, season_start_year, team_abbreviation)
    return json_encoded_player_season_team_statistics