import datetime
import time
import logging
import json

from basketball_reference_web_scraper.setup_logging import setup_logging
from basketball_reference_web_scraper.models.player_season_statistics import PlayerSeasonStatistics
from basketball_reference_web_scraper.json_encoders.player_season_statistics import PlayerSeasonStatisticsJsonEncoder


class ParsedPlayerSeasonStatisticsReturner:

    def __init__(self):
        pass

    @staticmethod
    def return_raw_player_season_statistics(player_season_statistics_html):
        player_season_statistics_list = list()
        header_count = len(player_season_statistics_html.xpath('//tr[@class=""]/th//@data-stat'))
        player_html = player_season_statistics_html.xpath('//tr[@class="full_table"]/td')
        count = 0
        while count < len(player_html):
            start = count
            stop = count + header_count
            player_season_statistics_list.append([player_season_statistics_element.text_content() for player_season_statistics_element in player_html[start:stop]])
            count = stop
        return player_season_statistics_list

    @staticmethod
    def return_all_player_season_statistics(player_season_statistics_html, season_start_year):
        # TODO: currently hard-coded should probably change in the future
        setup_logging()
        logging.getLogger()
        logging.info("starting to parse season statistics for {0}".format(season_start_year))
        raw_player_season_statistics_list = ParsedPlayerSeasonStatisticsReturner.return_raw_player_season_statistics(player_season_statistics_html)
        all_player_season_statistics = list()
        for raw_player_season_statistics in raw_player_season_statistics_list:
            # in case of total combined statistics
            if raw_player_season_statistics[4] != 'TOT':
                full_name = raw_player_season_statistics[1]
                first_name = full_name.split(" ")[0]
                last_name = full_name.split(" ")[1]
                player_season_statistics = PlayerSeasonStatistics(
                    first_name,
                    last_name,
                    raw_player_season_statistics[3],
                    raw_player_season_statistics[4],
                    raw_player_season_statistics[2],
                    raw_player_season_statistics[5],
                    raw_player_season_statistics[6],
                    raw_player_season_statistics[7],
                    raw_player_season_statistics[8],
                    raw_player_season_statistics[9],
                    raw_player_season_statistics[11],
                    raw_player_season_statistics[12],
                    raw_player_season_statistics[14],
                    raw_player_season_statistics[15],
                    raw_player_season_statistics[18],
                    raw_player_season_statistics[19],
                    raw_player_season_statistics[21],
                    raw_player_season_statistics[22],
                    raw_player_season_statistics[24],
                    raw_player_season_statistics[25],
                    raw_player_season_statistics[26],
                    raw_player_season_statistics[27],
                    raw_player_season_statistics[28],
                    raw_player_season_statistics[29],
                )
                all_player_season_statistics.append(player_season_statistics)
        logging.info("finished parsing season_statistics for {0}".format(season_start_year))
        return all_player_season_statistics

    @staticmethod
    def return_json_encoded_all_player_season_statistics(player_season_statistics_html, season_start_year):
        # TODO: currently hard-coded should probably change in the future
        setup_logging()
        logging.getLogger()
        logging.info("starting to parse season statistics for {0}".format(season_start_year))
        raw_player_season_statistics_list = ParsedPlayerSeasonStatisticsReturner.return_raw_player_season_statistics(player_season_statistics_html)
        all_json_encoded_player_season_statistics = list()
        for raw_player_season_statistics in raw_player_season_statistics_list:
            # in case of total combined statistics
            if raw_player_season_statistics[4] != 'TOT':
                full_name = raw_player_season_statistics[1]
                first_name = full_name.split(" ")[0]
                last_name = full_name.split(" ")[1]
                player_season_statistics = PlayerSeasonStatistics(
                    first_name,
                    last_name,
                    raw_player_season_statistics[3],
                    raw_player_season_statistics[4],
                    raw_player_season_statistics[2],
                    raw_player_season_statistics[5],
                    raw_player_season_statistics[6],
                    raw_player_season_statistics[7],
                    raw_player_season_statistics[8],
                    raw_player_season_statistics[9],
                    raw_player_season_statistics[11],
                    raw_player_season_statistics[12],
                    raw_player_season_statistics[14],
                    raw_player_season_statistics[15],
                    raw_player_season_statistics[18],
                    raw_player_season_statistics[19],
                    raw_player_season_statistics[21],
                    raw_player_season_statistics[22],
                    raw_player_season_statistics[24],
                    raw_player_season_statistics[25],
                    raw_player_season_statistics[26],
                    raw_player_season_statistics[27],
                    raw_player_season_statistics[28],
                    raw_player_season_statistics[29],
                )
                all_json_encoded_player_season_statistics.append(json.dumps(player_season_statistics, cls=PlayerSeasonStatisticsJsonEncoder))
        logging.info("finished parsing season_statistics for {0}".format(season_start_year))
        return all_json_encoded_player_season_statistics

    @staticmethod
    def return_player_season_team_statistics(player_season_statistics_html, player_first_name, player_last_name, season_start_year, team_abbreviation):
        # TODO: currently hard-coded should probably change in the future
        setup_logging()
        logging.getLogger()
        logging.info("starting to parse season statistics for {0} - {1} - {2} - {3}".format(player_first_name, player_last_name, season_start_year, team_abbreviation))
        raw_player_season_statistics_list = ParsedPlayerSeasonStatisticsReturner.return_raw_player_season_statistics(player_season_statistics_html)
        player_season_team_statistics = list()
        for raw_player_season_statistics in raw_player_season_statistics_list:
            full_name = raw_player_season_statistics[1]
            first_name = full_name.split(" ")[0]
            last_name = full_name.split(" ")[1]
            if player_first_name.lower() == first_name.lower() and player_last_name.lower() == last_name.lower() and team_abbreviation.lower() == raw_player_season_statistics[4].lower():
                player_season_statistics = PlayerSeasonStatistics(
                    first_name,
                    last_name,
                    raw_player_season_statistics[4],
                    raw_player_season_statistics[3],
                    raw_player_season_statistics[2],
                    raw_player_season_statistics[5],
                    raw_player_season_statistics[6],
                    raw_player_season_statistics[7],
                    raw_player_season_statistics[8],
                    raw_player_season_statistics[9],
                    raw_player_season_statistics[11],
                    raw_player_season_statistics[12],
                    raw_player_season_statistics[14],
                    raw_player_season_statistics[15],
                    raw_player_season_statistics[18],
                    raw_player_season_statistics[19],
                    raw_player_season_statistics[21],
                    raw_player_season_statistics[22],
                    raw_player_season_statistics[24],
                    raw_player_season_statistics[25],
                    raw_player_season_statistics[26],
                    raw_player_season_statistics[27],
                    raw_player_season_statistics[28],
                    raw_player_season_statistics[29],
                )
                player_season_team_statistics.append(player_season_statistics)
        logging.info("finished parsing season_statistics for {0}".format(season_start_year))
        return player_season_team_statistics

    @staticmethod
    def return_json_encoded_player_season_team_statistics(player_season_statistics_html, player_first_name, player_last_name, season_start_year, team_abbreviation):
        # TODO: currently hard-coded should probably change in the future
        setup_logging()
        logging.getLogger()
        logging.info("starting to parse season statistics for {0} - {1} - {2} - {3}".format(player_first_name, player_last_name, season_start_year, team_abbreviation))
        raw_player_season_statistics_list = ParsedPlayerSeasonStatisticsReturner.return_raw_player_season_statistics(player_season_statistics_html)
        json_encoded_player_season_team_statistics = list()
        for raw_player_season_statistics in raw_player_season_statistics_list:
            full_name = raw_player_season_statistics[1]
            first_name = full_name.split(" ")[0]
            last_name = full_name.split(" ")[1]
            if player_first_name.lower() == first_name.lower() and player_last_name.lower() == last_name.lower() and team_abbreviation.lower() == raw_player_season_statistics[4].lower():
                player_season_statistics = PlayerSeasonStatistics(
                    first_name,
                    last_name,
                    raw_player_season_statistics[3],
                    raw_player_season_statistics[4],
                    raw_player_season_statistics[2],
                    raw_player_season_statistics[5],
                    raw_player_season_statistics[6],
                    raw_player_season_statistics[7],
                    raw_player_season_statistics[8],
                    raw_player_season_statistics[9],
                    raw_player_season_statistics[11],
                    raw_player_season_statistics[12],
                    raw_player_season_statistics[14],
                    raw_player_season_statistics[15],
                    raw_player_season_statistics[18],
                    raw_player_season_statistics[19],
                    raw_player_season_statistics[21],
                    raw_player_season_statistics[22],
                    raw_player_season_statistics[24],
                    raw_player_season_statistics[25],
                    raw_player_season_statistics[26],
                    raw_player_season_statistics[27],
                    raw_player_season_statistics[28],
                    raw_player_season_statistics[29],
                )
                json_encoded_player_season_team_statistics.append(json.dumps(player_season_statistics, cls=PlayerSeasonStatisticsJsonEncoder))
        logging.info("finished parsing season_statistics for {0}".format(season_start_year))
        return json_encoded_player_season_team_statistics
