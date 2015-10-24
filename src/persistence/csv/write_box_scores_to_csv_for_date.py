from src.web_scraping.basketball_reference.box_scores.nba.box_score_web_scraper import BoxScoreWebScraper
from src.persistence.csv.box_scores_csv_writer import BoxScoresCsvWriter
from src.web_scraping.basketball_reference.schedule.nba.schedule_web_scraper import ScheduleWebScraper
import os
import pytz
import datetime


def write_box_scores_to_csv_for_date(date):
    file_directory = os.path.dirname(os.path.realpath('__file__'))
    box_scores = BoxScoreWebScraper.return_box_scores_for_date(date=date)
    file_to_write = os.path.join(file_directory, "box_scores/{0}.csv".format(date.strftime("%Y_%m_%d")))
    box_scores_csv_writer = BoxScoresCsvWriter()
    box_scores_csv_writer.write_to_csv(box_scores=box_scores, output_file_path=file_to_write)


def write_box_scores_to_csv_for_season(season_start_year):
    schedule = ScheduleWebScraper.return_event_list(season_start_year + 1)
    start_dates = sorted(set([event.start_time.astimezone(pytz.timezone("US/Eastern")).date() for event in schedule.parsed_event_list]))
    for start_date in start_dates:
        write_box_scores_to_csv_for_date(start_date)


def write_box_scores_to_csv_from_start_season_to_end_season(start_season_start_year, end_season_start_year):
    for start_year in range(start_season_start_year, end_season_start_year + 1):
        write_box_scores_to_csv_for_season(start_year)


write_box_scores_to_csv_from_start_season_to_end_season(2014, 2014)