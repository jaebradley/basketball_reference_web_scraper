from basketball_reference_web_scraper.html import PlayerContractsRow
from unittest import TestCase
from lxml import html


class TestPlayerContractsRow(TestCase):
    def test_final_contract_year_player(self):
        row = PlayerContractsRow(html=html.fromstring(
            """
            <tr><th scope="row" class="right " data-stat="ranker" csk="21">21</th><td class="left " data-append-csv="siakapa01" data-stat="player"><a href="/players/s/siakapa01.html"></a><a href="/players/s/siakapa01.html">Pascal Siakam</a></td><td class="left " data-stat="team_id"><a href="/contracts/IND.html">IND</a></td><td class="right " data-stat="y1" csk="37893408">$37,893,408</td><td class="right iz" data-stat="y2"></td><td class="right iz" data-stat="y3"></td><td class="right iz" data-stat="y4"></td><td class="right iz" data-stat="y5"></td><td class="right iz" data-stat="y6"></td><td class="right " data-stat="remain_gtd" csk="37893408">$37,893,408</td></tr>
            """
        ))

        self.assertIsNotNone(row)
        self.assertEqual("Pascal Siakam", row.player_name)
        self.assertEqual("IND", row.team_abbreviation)
        self.assertEqual(("37893408", "right "), row.first_contract_year_data)