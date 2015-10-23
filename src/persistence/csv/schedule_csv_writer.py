import csv


class ScheduleCsvWriter:
    def __init__(self):
        self.output_file_path = "../schedules/"

    def write_to_csv(self, schedule):
        with open("{0}{1}_{2}.csv".format(self.output_file_path, schedule.start_year, schedule.end_year), "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(
                (
                    event.start_time,
                    event.home_team_name,
                    event.visiting_team_name
                ) for event in schedule.parsed_event_list
            )