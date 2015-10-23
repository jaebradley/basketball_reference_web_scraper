from src.web_scraping.basketball_reference.box_scores.box_score_url_generator import BoxScoreUrlGenerator
from src.web_scraping.basketball_reference.box_scores.box_scores_html_returner import BoxScoresHtmlReturner
from src.persistence.model.box_score import BoxScore

import datetime
import time


class ParsedBoxScoresReturner:

    def __init__(self):
        pass

    @staticmethod
    def return_raw_box_score_list_of_lists(box_scores_html):
        box_scores_list = list()
        header_count = len(box_scores_html.xpath('//tr[@class=""]/th//@data-stat'))
        player_html = box_scores_html.xpath('//tr[@class=""]/td')
        count = 0
        while count < len(player_html):
            start = count
            stop = count + header_count
            box_scores_list.append([box_score_element.text_content() for box_score_element in player_html[start:stop]])
            count = stop
        return box_scores_list

    def return_box_scores(self, box_scores_html, date):
        # TODO: currently hard-coded should probably change in the future
        box_score_list_of_lists = self.return_raw_box_score_list_of_lists(box_scores_html)
        box_scores = list()
        for box_score_list in box_score_list_of_lists:
            full_name = box_score_list[1]
            first_name = full_name.split(" ")[0]
            last_name = full_name.split(" ")[1]
            x = time.strptime(box_score_list[6], "%M:%S")
            seconds_played = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
            if "@" == box_score_list[3]:
                is_home = False
            else:
                is_home = True
            box_score = BoxScore(
                first_name,
                last_name,
                date,
                box_score_list[2],
                box_score_list[4],
                is_home,
                seconds_played,
                box_score_list[7],
                box_score_list[8],
                box_score_list[10],
                box_score_list[11],
                box_score_list[13],
                box_score_list[14],
                box_score_list[16],
                box_score_list[17],
                box_score_list[18],
                box_score_list[19],
                box_score_list[20],
                box_score_list[21],
                box_score_list[22],
                box_score_list[23],
                box_score_list[24]
            )
            box_scores.append(box_score)
        return box_scores