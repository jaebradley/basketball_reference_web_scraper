import datetime
from src.web_scraping.basketball_reference.box_scores.nba.box_score_web_scraper import BoxScoreWebScraper

date = datetime.datetime(year=2014, month=11, day=11)
print BoxScoreWebScraper.return_json_encoded_box_scores_for_date(date=date)
