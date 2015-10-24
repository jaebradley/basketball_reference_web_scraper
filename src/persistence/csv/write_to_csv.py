from src.persistence.csv.schedule_csv_writer import ScheduleCsvWriter
from src.web_scraping.basketball_reference.schedule.nba.schedule_web_scraper import ScheduleWebScraper
import os

file_directory = os.path.dirname(os.path.realpath('__file__'))
year = 2015
schedule = ScheduleWebScraper.return_event_list(year)
schedule_csv_writer = ScheduleCsvWriter()
file_to_write = os.path.join(file_directory, "schedules/{0}_{1}.csv".format(schedule.start_year, schedule.end_year))
schedule_csv_writer.write_to_csv(schedule, file_to_write)