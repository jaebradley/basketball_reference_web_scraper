import csv
import datetime


class CsvWriter:
    def __init__(self):
        self.output_file_path = "../box_scores/"

    def write_to_csv(self, boxscores):
        # TODO: find better solution than hard-coded
        date = boxscores[0].date
        date_string = date.strftime("%m_%d_%Y")
        with open("{0}{1}.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(
                (
                    boxscore.first_name,
                    boxscore.last_name,
                    boxscore.date,
                    boxscore.team,
                    boxscore.opponent,
                    boxscore.is_home,
                    boxscore.seconds_played,
                    boxscore.field_goals,
                    boxscore.field_goal_attempts,
                    boxscore.three_point_field_goals,
                    boxscore.three_point_field_goal_attempts,
                    boxscore.free_throws,
                    boxscore.offensive_rebounds,
                    boxscore.defensive_rebounds,
                    boxscore.total_rebounds,
                    boxscore.assists,
                    boxscore.steals,
                    boxscore.blocks,
                    boxscore.turnovers,
                    boxscore.personal_fouls,
                    boxscore.points
                ) for boxscore in boxscores
            )