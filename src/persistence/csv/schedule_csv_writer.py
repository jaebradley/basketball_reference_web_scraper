from src.web_scraping.basketball_reference.schedule.nba.schedule_web_scraper import ScheduleWebScraper
import csv
import os

class ScheduleCsvWriter:

    def __init__(self):
        pass

    @staticmethod
    def write_to_csv(schedule, output_file_path):
        with open(output_file_path, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(
                (
                    event.start_time,
                    event.home_team_name,
                    event.visiting_team_name
                ) for event in schedule.parsed_event_list
            )

    @staticmethod
    def write_schedule_to_csv_for_seasons_in_range(start_year, end_year):
        file_directory = os.path.dirname(os.path.realpath('__file__'))
        schedule_csv_writer = ScheduleCsvWriter()
        for year in range(start_year, end_year + 1):
            schedule = ScheduleWebScraper.return_event_list(year)
            file_to_write = os.path.join(file_directory, "schedules/{0}_{1}.csv".format(schedule.start_year, schedule.end_year))
            schedule_csv_writer.write_to_csv(schedule, file_to_write)