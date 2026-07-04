

class PlayerShootingStatisticRow:
    def __init__(self, html):
        self.html = html

    @property
    def position_abbreviation(self):
        cells = self.html.xpath('td[@data-stat="pos"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def age(self):
        cells = self.html.xpath('td[@data-stat="age"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def games_played(self):
        cells = self.html.xpath('td[@data-stat="games"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def games_started(self):
        cells = self.html.xpath('td[@data-stat="games_started"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def is_combined_totals(self):
        #  No longer says 'TOT' - now says 2TM, 3TM, etc.
        # Can safely use the 'TM' suffix as an identifier as no team abbreviations
        # end in 'TM'
        return self.team_abbreviation.endswith("TM")

    @property
    def team_abbreviation(self):
        cells = self.html.xpath('td[@data-stat="team_name_abbr"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def player_cell(self):
        cells = self.html.xpath('td[@data-stat="name_display"]')

        if len(cells) > 0:
            return cells[0]

        return None

    @property
    def slug(self):
        cell = self.player_cell
        if cell is None:
            return ''

        return cell.get('data-append-csv')

    @property
    def name(self):
        cell = self.player_cell
        if cell is None:
            return ''

        return cell.text_content()

    @property
    def minutes_played(self):
        cells = self.html.xpath('td[@data-stat="mp"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def field_goal_percentage(self):
        cells = self.html.xpath('td[@data-stat="fg_pct"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def average_field_goal_attempt_distance_in_feet(self):
        cells = self.html.xpath('td[@data-stat="avg_dist"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def percentage_of_field_goal_attempts_that_were_two_pointers(self):
        cells = self.html.xpath('td[@data-stat="pct_fga_fg2a"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def percentage_of_field_goal_attempts_zero_to_three_feet_from_the_basket(self):
        cells = self.html.xpath('td[@data-stat="pct_fga_00_03"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def percentage_of_field_goal_attempts_three_to_ten_feet_from_the_basket(self):
        cells = self.html.xpath('td[@data-stat="pct_fga_03_10"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def percentage_of_field_goal_attempts_ten_to_sixteen_feet_from_the_basket(self):
        cells = self.html.xpath('td[@data-stat="pct_fga_10_16"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def percentage_of_field_goal_attempts_sixteen_feet_from_the_basket_to_three_point_line(self):
        cells = self.html.xpath('td[@data-stat="pct_fga_16_xx"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def percentage_of_field_goal_attempts_that_were_three_pointers(self):
        cells = self.html.xpath('td[@data-stat="pct_fga_fg3a"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def two_point_field_goal_percentage(self):
        cells = self.html.xpath('td[@data-stat="fg_pct_fg2a"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def zero_to_three_feet_from_the_basket_field_goal_percentage(self):
        cells = self.html.xpath('td[@data-stat="fg_pct_00_03"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def three_to_ten_feet_from_the_basket_field_goal_percentage(self):
        cells = self.html.xpath('td[@data-stat="fg_pct_03_10"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def ten_to_sixteen_feet_from_the_basket_field_goal_percentage(self):
        cells = self.html.xpath('td[@data-stat="fg_pct_10_16"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def sixteen_to_three_point_line_field_goal_percentage(self):
        cells = self.html.xpath('td[@data-stat="fg_pct_16_xx"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def three_point_field_goal_percentage(self):
        cells = self.html.xpath('td[@data-stat="fg_pct_fg3a"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def percentage_of_two_pointers_that_were_assisted(self):
        cells = self.html.xpath('td[@data-stat="pct_ast_fg2"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def percentage_of_three_pointers_that_were_assisted(self):
        cells = self.html.xpath('td[@data-stat="pct_ast_fg3"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def percentage_of_field_goal_attempts_that_were_dunks(self):
        cells = self.html.xpath('td[@data-stat="pct_fga_dunk"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def made_dunks(self):
        cells = self.html.xpath('td[@data-stat="fg_dunk"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def percentage_of_three_point_attempts_that_were_corner_threes(self):
        cells = self.html.xpath('td[@data-stat="pct_fg3a_corner3"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def corner_three_field_goal_percentage(self):
        cells = self.html.xpath('td[@data-stat="fg_pct_corner3"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def beyond_half_court_attempts(self):
        cells = self.html.xpath('td[@data-stat="fg3a_heave"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def made_beyond_half_court_shots(self):
        cells = self.html.xpath('td[@data-stat="fg3_heave"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

class PlayersSeasonShootingStatisticsTable:
    def __init__(self, html):
        self.html = html

    @property
    def rows_query(self):
        # Basketball Reference includes individual rows for players that played for multiple teams in a season.
        # It also includes a "League Average" row that has a class value of 'norank'.
        return """
                    //table[@id='shooting']
                    /tbody
                    /tr[
                        not(contains(@class, 'thead')) and 
                        not(contains(@class, 'norank'))
                    ]
                """

    @property
    def rows(self) -> list[PlayerShootingStatisticRow]:
        players_shooting_statistics_rows = []
        for row_html in self.html.xpath(self.rows_query):
            row = PlayerShootingStatisticRow(html=row_html)
            # Basketball Reference includes a "total" row for players that got traded
            # which is essentially a sum of all player team rows
            # I want to avoid including those, so I check the "team" field value for "TOT"
            if not row.is_combined_totals:
                players_shooting_statistics_rows.append(row)
        return players_shooting_statistics_rows
