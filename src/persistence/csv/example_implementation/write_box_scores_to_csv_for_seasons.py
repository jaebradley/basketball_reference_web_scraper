from src.persistence.csv.box_scores_csv_writer import BoxScoresCsvWriter

# writes box scores to src/persistence/csv/box_scores as csv files for the given start season start year and end season start year
BoxScoresCsvWriter.write_box_scores_to_csv_from_start_season_to_end_season(2014, 2014)