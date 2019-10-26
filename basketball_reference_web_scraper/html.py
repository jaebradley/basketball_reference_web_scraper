import re


class PlayerSeasonTotalTable:
    def __init__(self, html):
        self.html = html

    @property
    def rows_query(self):
        # Basketball Reference includes individual rows for players that played for multiple teams in a season
        # These rows have a separate class ("italic_text partial_table") than the players that played for a single team
        # across a season.
        return """
            //table[@id="totals_stats"]
            /tbody
            /tr[
                contains(@class, "full_table") or 
                contains(@class, "italic_text partial_table") 
                and not(contains(@class, "rowSum"))
            ]
        """

    @property
    def rows(self):
        player_season_totals_rows = []
        for row_html in self.html.xpath(self.rows_query):
            row = PlayerSeasonTotalRow(html=row_html)
            # Basketball Reference includes a "total" row for players that got traded
            # which is essentially a sum of all player team rows
            # I want to avoid including those, so I check the "team" field value for "TOT"
            if not row.is_combined_totals:
                player_season_totals_rows.append(row)

        return player_season_totals_rows


class PlayerSeasonTotalRow:
    def __init__(self, html):
        self.html = html

    @property
    def player_name_cell(self):
        return self.html[1]

    @property
    def slug(self):
        return self.player_name_cell.get('data-append-csv')

    @property
    def name(self):
        return self.player_name_cell.text_content()

    @property
    def position_abbreviations(self):
        return self.html[2].text_content()

    @property
    def age(self):
        return self.html[3].text_content()

    @property
    def team_abbreviation(self):
        return self.html[4].text_content()

    @property
    def games_played(self):
        return self.html[5].text_content()

    @property
    def games_started(self):
        return self.html[6].text_content()

    @property
    def minutes_played(self):
        return self.html[7].text_content()

    @property
    def made_field_goals(self):
        return self.html[8].text_content()

    @property
    def attempted_field_goals(self):
        return self.html[9].text_content()

    @property
    def made_three_point_field_goals(self):
        return self.html[11].text_content()

    @property
    def attempted_three_point_field_goals(self):
        return self.html[12].text_content()

    @property
    def made_free_throws(self):
        return self.html[18].text_content()

    @property
    def attempted_free_throws(self):
        return self.html[19].text_content()

    @property
    def offensive_rebounds(self):
        return self.html[21].text_content()

    @property
    def defensive_rebounds(self):
        return self.html[22].text_content()

    @property
    def assists(self):
        return self.html[24].text_content()

    @property
    def steals(self):
        return self.html[25].text_content()

    @property
    def blocks(self):
        return self.html[26].text_content()

    @property
    def turnovers(self):
        return self.html[27].text_content()

    @property
    def personal_fouls(self):
        return self.html[28].text_content()

    @property
    def is_combined_totals(self):
        return self.html[4].text_content() == "TOT"


class BoxScoresPage:
    def __init__(self, html):
        self.html = html

    @property
    def statistics_tables(self):
        return [
            StatisticsTable(table_html)
            for table_html in self.html.xpath('//table[contains(@class, "stats_table")]')
        ]

    @property
    def basic_statistics_tables(self):
        return [
            table
            for table in self.statistics_tables
            if table.has_basic_statistics is True
        ]


class StatisticsTable:
    def __init__(self, html):
        self.html = html

    @property
    def has_basic_statistics(self):
        return 'game-basic' in self.html.attrib["id"]

    @property
    def team_abbreviation(self):
        # Example id value is box-BOS-game-basic or box-BOS-game-advanced
        match = re.match('^box-(.+)-game', self.html.attrib["id"])
        return match.group(1)

    @property
    def team_totals(self):
        # Team totals are stored as table footers
        return TeamTotalRow(self.html.xpath('tfoot/tr/td'))


class TeamTotalRow:
    def __init__(self, html):
        self.html = html

    @property
    def minutes_played(self):
        return self.html[0].text_content()

    @property
    def made_field_goals(self):
        return self.html[1].text_content()

    @property
    def attempted_field_goals(self):
        return self.html[2].text_content()

    @property
    def made_three_point_field_goals(self):
        return self.html[4].text_content()

    @property
    def attempted_three_point_field_goals(self):
        return self.html[5].text_content()

    @property
    def made_free_throws(self):
        return self.html[7].text_content()

    @property
    def attempted_free_throws(self):
        return self.html[8].text_content()

    @property
    def offensive_rebounds(self):
        return self.html[10].text_content()

    @property
    def defensive_rebounds(self):
        return self.html[11].text_content()

    @property
    def assists(self):
        return self.html[13].text_content()

    @property
    def steals(self):
        return self.html[14].text_content()

    @property
    def blocks(self):
        return self.html[15].text_content()

    @property
    def turnovers(self):
        return self.html[16].text_content()

    @property
    def personal_fouls(self):
        return self.html[17].text_content()


class DailyLeadersPage:
    def __init__(self, html):
        self.html = html

    @property
    def daily_leaders(self):
        return [
            PlayerBoxScoreRow(row_html)
            for row_html in self.html.xpath('//table[@id="stats"]//tbody/tr[not(contains(@class, "thead"))]')
        ]


class PlayerBoxScoreRow:
    def __init__(self, html):
        self.html = html

    @property
    def slug(self):
        return self.html[1].get('data-append-csv')

    @property
    def name(self):
        return self.html[1].text_content()

    @property
    def team_abbreviation(self):
        return self.html[2].text_content()

    @property
    def location_abbreviation(self):
        return self.html[3].text_content()

    @property
    def opponent_abbreviation(self):
        return self.html[4].text_content()

    @property
    def outcome(self):
        return self.html[5].text_content()

    @property
    def playing_time(self):
        return self.html[6].text_content()

    @property
    def made_field_goals(self):
        return self.html[7].text_content()

    @property
    def attempted_field_goals(self):
        return self.html[8].text_content()

    @property
    def made_three_point_field_goals(self):
        return self.html[10].text_content()

    @property
    def attempted_three_point_field_goals(self):
        return self.html[11].text_content()

    @property
    def made_free_throws(self):
        return self.html[13].text_content()

    @property
    def attempted_free_throws(self):
        return self.html[14].text_content()

    @property
    def offensive_rebounds(self):
        return self.html[16].text_content()

    @property
    def defensive_rebounds(self):
        return self.html[17].text_content()

    @property
    def assists(self):
        return self.html[19].text_content()

    @property
    def steals(self):
        return self.html[20].text_content()

    @property
    def blocks(self):
        return self.html[21].text_content()

    @property
    def turnovers(self):
        return self.html[22].text_content()

    @property
    def personal_fouls(self):
        return self.html[23].text_content()

    @property
    def game_score(self):
        return self.html[26].text_content()
