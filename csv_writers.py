import csv
import os
import pytz
from basketball_reference_web_scraper.web_scrapers import return_schedule, return_box_scores_for_date


def write_schedule_data_to_csv(schedule, output_file_path):
        with open(output_file_path, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(
                (
                    event.start_time,
                    event.home_team_name,
                    event.visiting_team_name
                ) for event in schedule.parsed_event_list
            )


def write_schedule_to_csv_for_seasons_in_range(start_year, end_year):
    file_directory = os.path.dirname(os.path.realpath('__file__'))
    for year in range(start_year, end_year + 1):
        schedule = return_schedule(year)
        file_to_write = os.path.join(file_directory, "schedules/{0}_{1}.csv".format(schedule.start_year, schedule.end_year))
        write_schedule_data_to_csv(schedule, file_to_write)


def write_box_scores_to_csv(box_scores, output_file_path):
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


def write_box_scores_to_csv_for_date(date):
    file_directory = os.path.dirname(os.path.realpath('__file__'))
    box_scores = return_box_scores_for_date(date=date)
    file_to_write = os.path.join(file_directory, "box_scores/{0}.csv".format(date.strftime("%Y_%m_%d")))
    write_box_scores_to_csv(box_scores=box_scores, output_file_path=file_to_write)


def write_box_scores_to_csv_for_season(season_start_year):
    schedule = return_schedule(season_start_year + 1)
    start_dates = sorted(set([event.start_time.astimezone(pytz.timezone("US/Eastern")).date() for event in schedule.parsed_event_list]))
    for start_date in start_dates:
        write_box_scores_to_csv_for_date(start_date)


def write_box_scores_to_csv_from_start_season_to_end_season(start_season_start_year, end_season_start_year):
    for start_year in range(start_season_start_year, end_season_start_year + 1):
        write_box_scores_to_csv_for_season(start_year)