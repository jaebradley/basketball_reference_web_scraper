from src.web_scraping.basketball_reference.box_scores.nba.parsed_box_scores_returner import ParsedBoxScoresReturner
from src.persistence.csv.box_scores_csv_writer import BoxScoresCsvWriter
import os


def write_box_scores_to_csv_for_date(date):
    file_directory = os.path.dirname(os.path.realpath('__file__'))
    box_scores_csv_writer = BoxScoresCsvWriter()
    box_scores_csv_writer.write_to_csv()
