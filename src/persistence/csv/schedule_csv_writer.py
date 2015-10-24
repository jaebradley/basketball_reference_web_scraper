import csv


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