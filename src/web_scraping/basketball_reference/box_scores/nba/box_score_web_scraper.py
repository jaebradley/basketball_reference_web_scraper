from src.web_scraping.basketball_reference.box_scores.nba.box_score_url_generator import BoxScoreUrlGenerator
from src.web_scraping.basketball_reference.box_scores.nba.box_scores_html_returner import BoxScoresHtmlReturner
from src.web_scraping.basketball_reference.box_scores.nba.parsed_box_scores_returner import ParsedBoxScoresReturner


class BoxScoreWebScraper:
    def __init__(self):
        pass

    @staticmethod
    def return_box_scores_for_date(date):
        generated_url = BoxScoreUrlGenerator.generate_url(date=date)
        raw_box_scores_html = BoxScoresHtmlReturner.return_html(box_score_url=generated_url)
        box_scores = ParsedBoxScoresReturner.return_box_scores(box_scores_html=raw_box_scores_html, date=date)
        return box_scores

    @staticmethod
    def return_json_encoded_box_scores_for_date(date):
        generated_url = BoxScoreUrlGenerator.generate_url(date=date)
        raw_box_scores_html = BoxScoresHtmlReturner.return_html(box_score_url=generated_url)
        json_encoded_box_scores = ParsedBoxScoresReturner.return_json_encoded_box_scores(box_scores_html=raw_box_scores_html, date=date)
        return json_encoded_box_scores