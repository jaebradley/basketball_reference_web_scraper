from src.persistence.csv.schedule_csv_writer import ScheduleCsvWriter
from src.web_scraping.basketball_reference.schedule.nba.schedule_web_scraper import ScheduleWebScraper

year = 2015
schedule = ScheduleWebScraper.return_event_list(year)
schedule_csv_writer = ScheduleCsvWriter()
schedule_csv_writer.write_to_csv(schedule, "../schedules/{0}_{1}.csv".format(schedule.start_year, schedule.end_year))