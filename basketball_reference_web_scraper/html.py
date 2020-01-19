import re


class PlayerAdvancedSeasonTotalsTable:
    def __init__(self, html):
        self.html = html

    @property
    def rows_query(self):
        return """
            //table[@id="advanced_stats"]
            /tbody
            /tr[
                contains(@class, "full_table") or 
                contains(@class, "italic_text partial_table") 
                and not(contains(@class, "rowSum"))
            ]
        """

    @property
    def rows(self):
        player_advanced_season_totals_rows = []
        for row_html in self.html.xpath(self.rows_query):
            row = PlayerAdvancedSeasonTotalsRow(html=row_html)
            if not row.is_combined_totals:
                # Basketball Reference includes a "total" row for players that got traded
                # which is essentially a sum of all player team rows
                # I want to avoid including those, so I check the "team" field value for "TOT"
                player_advanced_season_totals_rows.append(row)

        return player_advanced_season_totals_rows


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


class PlayerAdvancedSeasonTotalsRow:
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
    def minutes_played(self):
        return self.html[6].text_content()

    @property
    def player_efficiency_rating(self):
        return self.html[7].text_content()

    @property
    def true_shooting_percentage(self):
        return self.html[8].text_content()

    @property
    def three_point_attempt_rate(self):
        return self.html[9].text_content()

    @property
    def free_throw_attempt_rate(self):
        return self.html[10].text_content()

    @property
    def offensive_rebound_percentage(self):
        return self.html[11].text_content()

    @property
    def defensive_rebound_percentage(self):
        return self.html[12].text_content()

    @property
    def total_rebound_percentage(self):
        return self.html[13].text_content()

    @property
    def assist_percentage(self):
        return self.html[14].text_content()

    @property
    def steal_percentage(self):
        return self.html[15].text_content()

    @property
    def block_percentage(self):
        return self.html[16].text_content()

    @property
    def turnover_percentage(self):
        return self.html[17].text_content()

    @property
    def usage_percentage(self):
        return self.html[18].text_content()

    @property
    def offensive_win_shares(self):
        return self.html[20].text_content()

    @property
    def defensive_win_shares(self):
        return self.html[21].text_content()

    @property
    def win_shares(self):
        return self.html[22].text_content()

    @property
    def win_shares_per_48_minutes(self):
        return self.html[23].text_content()

    @property
    def offensive_plus_minus(self):
        return self.html[25].text_content()

    @property
    def defensive_plus_minus(self):
        return self.html[26].text_content()

    @property
    def plus_minus(self):
        return self.html[27].text_content()

    @property
    def value_over_replacement_player(self):
        return self.html[28].text_content()

    @property
    def is_combined_totals(self):
        return self.team_abbreviation == "TOT"


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


class PlayByPlayPage:
    def __init__(self, html):
        self.html = html

    @property
    def table_query(self):
        return '//table[@id="pbp"]'

    @property
    def team_names_query(self):
        return \
            '//*[@id="content"]' \
            '//div[@class="scorebox"]' \
            '//div[@itemprop="performer"]' \
            '//a[@itemprop="name"]'

    @property
    def play_by_play_table(self):
        return PlayByPlayTable(html=self.html.xpath(self.table_query)[0])

    @property
    def team_names(self):
        names = self.html.xpath(self.team_names_query)

        return [
            name.text_content()
            for name in names
        ]

    @property
    def away_team_name(self):
        return self.team_names[0]

    @property
    def home_team_name(self):
        return self.team_names[1]


class PlayByPlayTable:
    def __init__(self, html):
        self.html = html

    @property
    def rows(self):
        return [
            PlayByPlayRow(html=row_html)
            # Ignore first row in table
            for row_html in self.html[1:]
        ]


class PlayByPlayRow:
    def __init__(self, html):
        self.html = html

    @property
    def timestamp_cell(self):
        return self.html[0]

    @property
    def timestamp(self):
        return self.timestamp_cell.text_content().strip()

    @property
    def away_team_play_description(self):
        return self.html[1].text_content().strip()

    @property
    def home_team_play_description(self):
        return self.html[5].text_content().strip()

    @property
    def is_away_team_play(self):
        return self.away_team_play_description != ""

    @property
    def is_home_team_play(self):
        return self.home_team_play_description != ""

    @property
    def formatted_scores(self):
        return self.html[3].text_content().strip()

    @property
    def is_start_of_period(self):
        return self.timestamp_cell.get('colspan') == '6'

    @property
    def has_play_by_play_data(self):
        # TODO: @jaebradley refactor this to be slightly clearer
        # Need to avoid rows that indicate start of period
        # Or denote tipoff / end of period (colspan = 5)
        # Or are one of the table headers for each period group (aria-label = Time)
        return not self.is_start_of_period \
               and self.html[1].get('colspan') != '5' \
               and self.timestamp_cell.get('aria-label') != 'Time'
