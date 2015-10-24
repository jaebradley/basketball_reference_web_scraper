from src.persistence.csv.schedule_csv_writer import ScheduleCsvWriter

# writes schedule to csv file in src/persistence/csv/schedules directory
ScheduleCsvWriter.write_schedule_to_csv_for_seasons_in_range(2013, 2013)