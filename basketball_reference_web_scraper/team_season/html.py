from basketball_reference_web_scraper.html import PlayerIdentificationRow


class TeamSeasonPage:
    def __init__(self, html):
        self.html = html

    @property
    def roster_rows_query(self):
        return '//table[@id="roster"]//tbody//tr'

    @property
    def roster_rows(self):
        return [
            RosterRow(html=row_html)
            for row_html in self.html.xpath(self.roster_rows_query)
        ]


class RosterRow(PlayerIdentificationRow):
    def __init__(self, html):
        super().__init__(html=html)

    @property
    def player_url(self):
        if self.player_cell is None:
            return ''

        urls = self.player_cell.xpath('a')
        if len(urls) == 1:
            return urls[0].get('href')

        return ''

    @property
    def number(self):
        cells = self.html.xpath('.//th[@data-stat="number"]')
        if len(cells) == 1:
            return cells[0].text_content()

        return ''

    @property
    def position_abbreviation(self):
        cells = self.html.xpath('.//td[@data-stat="pos"]')
        if len(cells) == 1:
            return cells[0].text_content()

        return ''
