from src.web_scraping.basketball_reference.box_scores.nba.box_score_web_scraper import BoxScoreWebScraper
from src.web_scraping.basketball_reference.schedule.nba.schedule_web_scraper import ScheduleWebScraper
import os
import pytz
import csv


class BoxScoresCsvWriter:
    def __init__(self):
        pass

    @staticmethod
    def write_to_csv(box_scores, output_file_path):
        # TODO: find better solution than hard-coded
        with open(output_file_path, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(
                (
                    box_score.first_name,
                    box_score.last_name,
                    box_score.date,
                    box_score.team,
                    box_score.opponent,
                    box_score.is_home,
                    box_score.seconds_played,
                    box_score.field_goals,
                    box_score.field_goal_attempts,
                    box_score.three_point_field_goals,
                    box_score.three_point_field_goal_attempts,
                    box_score.free_throws,
                    box_score.free_throw_attempts,
                    box_score.offensive_rebounds,
                    box_score.defensive_rebounds,
                    box_score.total_rebounds,
                    box_score.assists,
                    box_score.steals,
                    box_score.blocks,
                    box_score.turnovers,
                    box_score.personal_fouls,
                    box_score.points
                ) for box_score in box_scores
            )

    @staticmethod
    def write_box_scores_to_csv_for_date(date):
        file_directory = os.path.dirname(os.path.realpath('__file__'))
        box_scores = BoxScoreWebScraper.return_box_scores_for_date(date=date)
        file_to_write = os.path.join(file_directory, "box_scores/{0}.csv".format(date.strftime("%Y_%m_%d")))
        box_scores_csv_writer = BoxScoresCsvWriter()
        box_scores_csv_writer.write_to_csv(box_scores=box_scores, output_file_path=file_to_write)

    @staticmethod
    def write_box_scores_to_csv_for_season(season_start_year):
        schedule = ScheduleWebScraper.return_event_list(season_start_year + 1)
        start_dates = sorted(set([event.start_time.astimezone(pytz.timezone("US/Eastern")).date() for event in schedule.parsed_event_list]))
        for start_date in start_dates:
            BoxScoresCsvWriter.write_box_scores_to_csv_for_date(start_date)

    @staticmethod
    def write_box_scores_to_csv_from_start_season_to_end_season(start_season_start_year, end_season_start_year):
        for start_year in range(start_season_start_year, end_season_start_year + 1):
            BoxScoresCsvWriter.write_box_scores_to_csv_for_season(start_year)