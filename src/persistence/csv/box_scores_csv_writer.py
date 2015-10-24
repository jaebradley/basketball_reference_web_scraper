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