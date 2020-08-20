import re
from lxml import html
from lxml.html import HtmlComment


class BasicBoxScoreRow:
    def __init__(self, html):
        self.html = html

    @property
    def playing_time(self):
        cells = self.html.xpath('td[@data-stat="mp"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def minutes_played(self):
        return self.playing_time

    @property
    def made_field_goals(self):
        cells = self.html.xpath('td[@data-stat="fg"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def attempted_field_goals(self):
        cells = self.html.xpath('td[@data-stat="fga"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def made_three_point_field_goals(self):
        cells = self.html.xpath('td[@data-stat="fg3"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def attempted_three_point_field_goals(self):
        cells = self.html.xpath('td[@data-stat="fg3a"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def made_free_throws(self):
        cells = self.html.xpath('td[@data-stat="ft"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def attempted_free_throws(self):
        cells = self.html.xpath('td[@data-stat="fta"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def offensive_rebounds(self):
        cells = self.html.xpath('td[@data-stat="orb"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def defensive_rebounds(self):
        cells = self.html.xpath('td[@data-stat="drb"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def assists(self):
        cells = self.html.xpath('td[@data-stat="ast"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def steals(self):
        cells = self.html.xpath('td[@data-stat="stl"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def blocks(self):
        cells = self.html.xpath('td[@data-stat="blk"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def turnovers(self):
        cells = self.html.xpath('td[@data-stat="tov"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def personal_fouls(self):
        cells = self.html.xpath('td[@data-stat="pf"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def points(self):
        cells = self.html.xpath('td[@data-stat="pts"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''


class PlayerBoxScoreRow(BasicBoxScoreRow):
    def __init__(self, html):
        super().__init__(html=html)

    def __eq__(self, other):
        if isinstance(other, PlayerBoxScoreRow):
            return self.html == other.html
        return False

    @property
    def team_abbreviation(self):
        cells = self.html.xpath('td[@data-stat="team_id"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def location_abbreviation(self):
        cells = self.html.xpath('td[@data-stat="game_location"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def opponent_abbreviation(self):
        cells = self.html.xpath('td[@data-stat="opp_id"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def outcome(self):
        cells = self.html.xpath('td[@data-stat="game_result"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def plus_minus(self):
        cells = self.html.xpath('td[@data-stat="plus_minus"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def game_score(self):
        cells = self.html.xpath('td[@data-stat="game_score"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''


class PlayerIdentificationRow:
    def __init__(self, html):
        self.html = html

    @property
    def player_cell(self):
        cells = self.html.xpath('td[@data-stat="player"]')

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

    def get_rows(self, include_combined_totals=False):
        player_advanced_season_totals_rows = []
        for row_html in self.html.xpath(self.rows_query):
            row = PlayerAdvancedSeasonTotalsRow(html=row_html)
            if (include_combined_totals is True and row.is_combined_totals is True) or row.is_combined_totals is False:
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
            row = PlayerSeasonTotalsRow(html=row_html)
            # Basketball Reference includes a "total" row for players that got traded
            # which is essentially a sum of all player team rows
            # I want to avoid including those, so I check the "team" field value for "TOT"
            if not row.is_combined_totals:
                player_season_totals_rows.append(row)

        return player_season_totals_rows


class PlayerAdvancedSeasonTotalsRow(PlayerIdentificationRow):
    def __init__(self, html):
        super().__init__(html=html)

    @property
    def position_abbreviations(self):
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
    def team_abbreviation(self):
        cells = self.html.xpath('td[@data-stat="team_id"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def games_played(self):
        cells = self.html.xpath('td[@data-stat="g"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def minutes_played(self):
        cells = self.html.xpath('td[@data-stat="mp"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def player_efficiency_rating(self):
        cells = self.html.xpath('td[@data-stat="per"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def true_shooting_percentage(self):
        cells = self.html.xpath('td[@data-stat="ts_pct"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def three_point_attempt_rate(self):
        cells = self.html.xpath('td[@data-stat="fg3a_per_fga_pct"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def free_throw_attempt_rate(self):
        cells = self.html.xpath('td[@data-stat="fta_per_fga_pct"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def offensive_rebound_percentage(self):
        cells = self.html.xpath('td[@data-stat="orb_pct"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def defensive_rebound_percentage(self):
        cells = self.html.xpath('td[@data-stat="drb_pct"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def total_rebound_percentage(self):
        cells = self.html.xpath('td[@data-stat="trb_pct"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def assist_percentage(self):
        cells = self.html.xpath('td[@data-stat="ast_pct"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def steal_percentage(self):
        cells = self.html.xpath('td[@data-stat="stl_pct"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def block_percentage(self):
        cells = self.html.xpath('td[@data-stat="blk_pct"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def turnover_percentage(self):
        cells = self.html.xpath('td[@data-stat="tov_pct"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def usage_percentage(self):
        cells = self.html.xpath('td[@data-stat="usg_pct"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def offensive_win_shares(self):
        cells = self.html.xpath('td[@data-stat="ows"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def defensive_win_shares(self):
        cells = self.html.xpath('td[@data-stat="dws"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def win_shares(self):
        cells = self.html.xpath('td[@data-stat="ws"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def win_shares_per_48_minutes(self):
        cells = self.html.xpath('td[@data-stat="ws_per_48"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def offensive_plus_minus(self):
        cells = self.html.xpath('td[@data-stat="obpm"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def defensive_plus_minus(self):
        cells = self.html.xpath('td[@data-stat="dbpm"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def plus_minus(self):
        cells = self.html.xpath('td[@data-stat="bpm"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def value_over_replacement_player(self):
        cells = self.html.xpath('td[@data-stat="vorp"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def is_combined_totals(self):
        return self.team_abbreviation == "TOT"


class PlayerSeasonTotalsRow(PlayerBoxScoreRow, PlayerIdentificationRow):
    def __init__(self, html):
        super().__init__(html=html)

    @property
    def position_abbreviations(self):
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
        cells = self.html.xpath('td[@data-stat="g"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def games_started(self):
        cells = self.html.xpath('td[@data-stat="gs"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def is_combined_totals(self):
        return self.team_abbreviation == "TOT"


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
        footers = self.html.xpath('tfoot/tr')
        if len(footers) > 0:
            return BasicBoxScoreRow(html=footers[0])

        return None


class DailyLeadersPage:
    def __init__(self, html):
        self.html = html

    @property
    def daily_leaders(self):
        return [
            PlayerGameBoxScoreRow(row_html)
            for row_html in self.html.xpath('//table[@id="stats"]//tbody/tr[not(contains(@class, "thead"))]')
        ]


class PlayerSeasonBoxScoresPage:
    def __init__(self, html):
        self.html = html

    @property
    def regular_season_box_scores_table_query(self):
        return '//table[@id="pgl_basic"]'

    @property
    def regular_season_box_scores_table(self):
        matching_tables = self.html.xpath(self.regular_season_box_scores_table_query)

        if len(matching_tables) != 1:
            return None

        return PlayerSeasonBoxScoresTable(html=matching_tables[0])

    @property
    def playoff_box_scores_table_container_query(self):
        return '//div[@id="all_pgl_basic_playoffs"]'

    """
    This is a limitation of requests as the playoff box scores table is "hidden" in a comment that is rendered later
    via some JavaScript.
    
    Because requests only fetches the raw HTML and doesn't process any JavaScript, this DOM element that (eventually)
    renders in the browser is not part of the HTML that is part of the initial fetched markup.
    
    Thus, the comment containing the playoff table is identified and parsed and then fed into lxml to create the element
    tree that will eventually be rendered on the page.
    """
    @property
    def playoff_box_scores_table(self):
        matching_containers = self.html.xpath(self.playoff_box_scores_table_container_query)

        if len(matching_containers) != 1:
            return None

        match = matching_containers[0]
        comments = [child for child in match.iter() if isinstance(child, HtmlComment)]

        if len(comments) != 1:
            return None

        first_comment = comments[0]

        try:
            playoff_table_html = re.search(r'(<!--)([\s\S]*?)(-->)', str(first_comment)).group(2).strip()
        except IndexError:
            return None

        tree = html.fromstring(playoff_table_html)

        matching_tables = tree.xpath('//table[@id="pgl_basic_playoffs"]')

        if len(matching_tables) != 1:
            return None

        return PlayerSeasonBoxScoresTable(html=matching_tables[0])


class PlayerSeasonBoxScoresTable:
    def __init__(self, html):
        self.html = html

    @property
    def rows_query(self):
        # Every 20 rows, there's a row that has the column header values - those should be ignored
        return '//tbody' \
               '/tr[not(contains(@class, "thead"))]'

    @property
    def rows(self):
        return [
            PlayerSeasonBoxScoresRow(html=row_html)
            for row_html in self.html.xpath(self.rows_query)
        ]


class PlayerSeasonBoxScoresRow(PlayerBoxScoreRow):
    def __init__(self, html):
        super().__init__(html)

    def __eq__(self, other):
        if isinstance(other, PlayerSeasonBoxScoresRow):
            return self.html == other.html
        return False

    @property
    def is_active(self):
        # When a player is not active (for a reason like "Inactive", "Did Not Play", "Did Not Dress")
        # the game played counter is blank (and a "reason" column will exist)
        cells = self.html.xpath('td[@data-stat="reason"]')
        return len(cells) < 1

    @property
    def date(self):
        cells = self.html.xpath('td[@data-stat="date_game"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def points_scored(self):
        cells = self.html.xpath('td[@data-stat="pts"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''


class PlayerGameBoxScoreRow(PlayerBoxScoreRow, PlayerIdentificationRow):
    def __init__(self, html):
        super().__init__(html)


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


class DailyBoxScoresPage:
    def __init__(self, html):
        self.html = html

    @property
    def game_url_paths_query(self):
        return '//td[contains(@class, "gamelink")]/a'

    @property
    def game_url_paths(self):
        game_links = self.html.xpath(self.game_url_paths_query)
        return [game_link.attrib['href'] for game_link in game_links]


class SchedulePage:
    def __init__(self, html):
        self.html = html

    @property
    def other_months_schedule_links_query(self):
        return '//div[@id="content"]' \
               '/div[@class="filter"]' \
               '/div[not(contains(@class, "current"))]' \
               '/a'

    @property
    def rows_query(self):
        return '//table[@id="schedule"]//tbody/tr'

    @property
    def other_months_schedule_urls(self):
        links = self.html.xpath(self.other_months_schedule_links_query)
        return [
            link.attrib['href']
            for link in links
        ]

    @property
    def rows(self):
        return [
            ScheduleRow(html=row)
            for row in self.html.xpath(self.rows_query)
            # Every row in each month's schedule table represents a game
            # except for the row where the only content is "Playoffs"
            if row.text_content() != 'Playoffs'
        ]


class ScheduleRow:
    def __init__(self, html):
        self.html = html

    def __eq__(self, other):
        if isinstance(other, ScheduleRow):
            return self.html == other.html
        return False

    @property
    def start_date(self):
        cells = self.html.xpath('th[@data-stat="date_game"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def start_time_of_day(self):
        cells = self.html.xpath('td[@data-stat="game_start_time"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def away_team_name(self):
        cells = self.html.xpath('td[@data-stat="visitor_team_name"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def home_team_name(self):
        cells = self.html.xpath('td[@data-stat="home_team_name"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def away_team_score(self):
        cells = self.html.xpath('td[@data-stat="visitor_pts"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def home_team_score(self):
        cells = self.html.xpath('td[@data-stat="home_pts"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''


class SearchPage:
    def __init__(self, html):
        self.html = html

    @property
    def nba_aba_baa_players_content_query(self):
        return '//div[@id="searches"]/div[@id="players"]'

    @property
    def nba_aba_baa_players_pagination_links_query(self):
        return '{NBA_ABA_PLAYERS_CONTENT_QUERY}/div[@class="search-pagination"]/a'.format(
            NBA_ABA_PLAYERS_CONTENT_QUERY=self.nba_aba_baa_players_content_query
        )

    @property
    def nba_aba_baa_player_search_items_query(self):
        return '{NBA_ABA_PLAYERS_CONTENT_QUERY}/div[@class="search-item"]'.format(
            NBA_ABA_PLAYERS_CONTENT_QUERY=self.nba_aba_baa_players_content_query
        )

    @property
    def nba_aba_baa_players_pagination_links(self):
        return self.html.xpath(self.nba_aba_baa_players_pagination_links_query)

    @property
    def nba_aba_baa_players_pagination_url(self):
        links = self.nba_aba_baa_players_pagination_links

        if len(links) <= 0:
            return None

        first_link = links[0]

        if len(links) == 1:
            if first_link.text_content() == 'Previous 100 Results':
                return None

            return first_link.attrib["href"]

        return links[1].attrib["href"]

    @property
    def nba_aba_baa_players(self):
        return [
            PlayerSearchResult(html=result_html)
            for result_html in self.html.xpath(self.nba_aba_baa_player_search_items_query)
        ]


class SearchResult:
    def __init__(self, html):
        self.html = html

    @property
    def resource_link_query(self):
        return './div[@class="search-item-name"]//a'

    @property
    def resource_link(self):
        links = self.html.xpath(self.resource_link_query)

        if len(links) > 0:
            return links[0]

        return None

    @property
    def resource_location(self):
        link = self.resource_link

        if link is None:
            return None

        return link.attrib["href"]

    @property
    def resource_name(self):
        link = self.resource_link

        if link is None:
            return None

        return link.text_content()

    def __eq__(self, other):
        if isinstance(other, SearchResult):
            return self.html == other.html
        return False


class PlayerSearchResult(SearchResult):
    @property
    def league_abbreviation_query(self):
        return './div[@class="search-item-league"]'

    @property
    def league_abbreviations(self):
        abbreviations = self.html.xpath(self.league_abbreviation_query)
        
        if len(abbreviations) > 0:
            return abbreviations[0].text_content()

        return None
    

class PlayerPageTotalsRow:
    def __init__(self, html):
        self.html = html
    
    @property
    def league_abbreviation(self):
        league_abbreviation_cells = self.html.xpath('.//td[@data-stat="lg_id"]')

        if len(league_abbreviation_cells) > 0:
            return league_abbreviation_cells[0].text_content()

        return None

    def __eq__(self, other):
        if isinstance(other, PlayerPageTotalsRow):
            return self.html == other.html
        return False


class PlayerPageTotalsTable:
    def __init__(self, html):
        self.html = html

    @property
    def rows(self):
        return [
            PlayerPageTotalsRow(html=row_html)
            for row_html in self.html.xpath('.//tbody/tr')
        ]

    def __eq__(self, other):
        if isinstance(other, PlayerPageTotalsTable):
            return self.html == other.html
        return False


class PlayerPage:
    def __init__(self, html):
        self.html = html
    
    @property
    def name(self):
        name_headers = self.html.xpath('.//h1[@itemprop="name"]')

        if len(name_headers) > 0:
            return name_headers[0].text_content().strip()

        return None

    @property
    def totals_table(self):
        totals_tables = self.html.xpath('.//table[@id="per_game"]')

        if len(totals_tables) > 0:
            return PlayerPageTotalsTable(html=totals_tables[0])

        return None


class StandingsPage:
    def __init__(self, html):
        self.html = html

    @property
    def division_standings(self):
        division_standings = self.html.xpath('.//div[@id="all_standings"]')

        if len(division_standings) == 1:
            return DivisionStandings(html=division_standings[0])

        return None


class DivisionStandings:
    def __init__(self, html):
        self.html = html

    @property
    def eastern_conference_table(self):
        tables = self.html.xpath('.//table[@id="divs_standings_E"]')

        if len(tables) == 1:
            return ConferenceDivisionStandingsTable(html=tables[0])

        return None

    @property
    def western_conference_table(self):
        tables = self.html.xpath('.//table[@id="divs_standings_W"]')

        if len(tables) == 1:
            return ConferenceDivisionStandingsTable(html=tables[0])

        return None


class ConferenceDivisionStandingsTable:
    def __init__(self, html):
        self.html = html

    @property
    def rows(self):
        return [
            ConferenceDivisionStandingsRow(html=row_html)
            for row_html in self.html.xpath('.//tbody/tr')
        ]


class ConferenceDivisionStandingsRow:
    def __init__(self, html):
        self.html = html

    @property
    def is_division_name_row(self):
        return self.html.attrib['class'] == 'thead'

    @property
    def is_standings_row(self):
        return self.html.attrib['class'] == 'full_table'

    @property
    def division_name(self):
        cells = self.html.xpath('.//th')

        if len(cells) == 1:
            return cells[0].text_content()

        return None

    @property
    def team_name(self):
        cells = self.html.xpath('.//th[@data-stat="team_name"]')

        if len(cells) == 1:
            return cells[0].text_content()

        return None

    @property
    def wins(self):
        cells = self.html.xpath('.//td[@data-stat="wins"]')

        if len(cells) == 1:
            return cells[0].text_content()

        return None

    @property
    def losses(self):
        cells = self.html.xpath('.//td[@data-stat="losses"]')

        if len(cells) == 1:
            return cells[0].text_content()

        return None
