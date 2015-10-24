import datetime
import time
import logging
import json

from basketball_reference_web_scraper.setup_logging import setup_logging
from basketball_reference_web_scraper.models.box_score import BoxScore
from basketball_reference_web_scraper.json_encoders.box_score import BoxScoreJsonEncoder


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

    @staticmethod
    def return_box_scores(box_scores_html, date):
        # TODO: currently hard-coded should probably change in the future
        setup_logging()
        logging.getLogger("main")
        logging.info("parsing box scores for {0}".format(date.strftime("%Y_%m_%d")))
        box_score_list_of_lists = ParsedBoxScoresReturner.return_raw_box_score_list_of_lists(box_scores_html)
        box_scores = list()
        for box_score_list in box_score_list_of_lists:
            full_name = box_score_list[1]
            first_name = full_name.split(" ")[0]
            last_name = full_name.split(" ")[1]
            if box_score_list[6] == '':
                seconds_played = 0
            else:
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
        logging.info("finished parsing box scores for {0}".format(date.strftime("%Y_%m_%d")))
        return box_scores

    @staticmethod
    def return_json_encoded_box_scores(box_scores_html, date):
        # TODO: currently hard-coded should probably change in the future
        setup_logging()
        logging.getLogger("main")
        logging.info("parsing box scores for {0}".format(date.strftime("%Y_%m_%d")))
        box_score_list_of_lists = ParsedBoxScoresReturner.return_raw_box_score_list_of_lists(box_scores_html)
        json_encoded_box_scores = list()
        for box_score_list in box_score_list_of_lists:
            full_name = box_score_list[1]
            first_name = full_name.split(" ")[0]
            last_name = full_name.split(" ")[1]
            if box_score_list[6] == '':
                seconds_played = 0
            else:
                x = time.strptime(box_score_list[6], "%M:%S")
                seconds_played = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
            if "@" == box_score_list[3]:
                is_home = False
            else:
                is_home = True
            box_score = BoxScore(
                first_name,
                last_name,
                str(date),
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
            json_encoded_box_scores.append(json.dumps(box_score, cls=BoxScoreJsonEncoder))
        logging.info("finished parsing box scores for {0}".format(date.strftime("%Y_%m_%d")))
        return json_encoded_box_scores