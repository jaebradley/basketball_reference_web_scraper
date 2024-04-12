from unittest import TestCase

from lxml import html

from basketball_reference_web_scraper.html import PlayerContractsRow


class TestPlayerContractsRow(TestCase):
    def test_final_contract_year_player(self):
        row = PlayerContractsRow(html=html.fromstring(
            """
            <tr><th scope="row" class="right " data-stat="ranker" csk="21">21</th><td class="left " data-append-csv="siakapa01" data-stat="player"><a href="/players/s/siakapa01.html"></a><a href="/players/s/siakapa01.html">Pascal Siakam</a></td><td class="left " data-stat="team_id"><a href="/contracts/IND.html">IND</a></td><td class="right " data-stat="y1" csk="37893408">$37,893,408</td><td class="right iz" data-stat="y2"></td><td class="right iz" data-stat="y3"></td><td class="right iz" data-stat="y4"></td><td class="right iz" data-stat="y5"></td><td class="right iz" data-stat="y6"></td><td class="right " data-stat="remain_gtd" csk="37893408">$37,893,408</td></tr>
            """
        ))

        self.assertIsNotNone(row)
        self.assertEqual("Pascal Siakam", row.player_name)
        self.assertEqual("siakapa01", row.player_identifier)
        self.assertEqual("IND", row.team_abbreviation)
        self.assertEqual(("$37,893,408", "right "), row.first_contract_year_data)
        self.assertEqual(("", "right iz"), row.second_contract_year_data)
        self.assertEqual(("", "right iz"), row.third_contract_year_data)
        self.assertEqual(("", "right iz"), row.fourth_contract_year_data)
        self.assertEqual(("", "right iz"), row.fifth_contract_year_data)
        self.assertEqual(("", "right iz"), row.sixth_contract_year_data)

    def test_player_with_no_empty_contract_years_and_no_team_or_player_options(self):
        row = PlayerContractsRow(html=html.fromstring(
            """
            <tr><th scope="row" class="right " data-stat="ranker" csk="41">41</th><td class="left " data-append-csv="brownja02" data-stat="player"><a href="/players/b/brownja02.html"></a><a href="/players/b/brownja02.html">Jaylen Brown</a></td><td class="left " data-stat="team_id"><a href="/contracts/BOS.html">BOS</a></td><td class="right " data-stat="y1" csk="31830357">$31,830,357</td><td class="right " data-stat="y2" csk="49700000">$49,700,000</td><td class="right " data-stat="y3" csk="53676000">$53,676,000</td><td class="right " data-stat="y4" csk="57652000">$57,652,000</td><td class="right " data-stat="y5" csk="61628000">$61,628,000</td><td class="right " data-stat="y6" csk="65604000">$65,604,000</td><td class="right " data-stat="remain_gtd" csk="320090357">$320,090,357</td></tr>
            """
        ))

        self.assertIsNotNone(row)
        self.assertEqual("Jaylen Brown", row.player_name)
        self.assertEqual("brownja02", row.player_identifier)
        self.assertEqual("BOS", row.team_abbreviation)
        self.assertEqual(("$31,830,357", "right "), row.first_contract_year_data)
        self.assertEqual(("$49,700,000", "right "), row.second_contract_year_data)
        self.assertEqual(("$53,676,000", "right "), row.third_contract_year_data)
        self.assertEqual(("$57,652,000", "right "), row.fourth_contract_year_data)
        self.assertEqual(("$61,628,000", "right "), row.fifth_contract_year_data)
        self.assertEqual(("$65,604,000", "right "), row.sixth_contract_year_data)

    def test_player_with_single_year_player_option(self):
        row = PlayerContractsRow(html=html.fromstring(
            """
            <tr><th scope="row" class="right " data-stat="ranker" csk="85">85</th><td class="left " data-append-csv="trentga02" data-stat="player"><a href="/players/t/trentga02.html"></a><a href="/players/t/trentga02.html">Gary Trent Jr.</a></td><td class="left " data-stat="team_id"><a href="/contracts/TOR.html">TOR</a></td><td class="right salary-pl" data-stat="y1" csk="18560000">$18,560,000</td><td class="right iz" data-stat="y2"></td><td class="right iz" data-stat="y3"></td><td class="right iz" data-stat="y4"></td><td class="right iz" data-stat="y5"></td><td class="right iz" data-stat="y6"></td><td class="right " data-stat="remain_gtd" csk="18560000">$18,560,000</td></tr>
            """
        ))

        self.assertEqual("Gary Trent Jr.", row.player_name)
        self.assertEqual("trentga02", row.player_identifier)
        self.assertEqual("TOR", row.team_abbreviation)
        self.assertEqual(("$18,560,000", "right salary-pl"), row.first_contract_year_data)
        self.assertEqual(("", "right iz"), row.second_contract_year_data)
        self.assertEqual(("", "right iz"), row.third_contract_year_data)
        self.assertEqual(("", "right iz"), row.fourth_contract_year_data)
        self.assertEqual(("", "right iz"), row.fifth_contract_year_data)
        self.assertEqual(("", "right iz"), row.sixth_contract_year_data)
        self.assertEqual("$18,560,000", row.guaranteed)

    def test_player_with_single_year_team_option(self):
        row = PlayerContractsRow(html=html.fromstring(
            """
            <tr><th scope="row" class="right " data-stat="ranker" csk="128">128</th><td class="left " data-append-csv="wisemja01" data-stat="player"><a href="/players/w/wisemja01.html"></a><a href="/players/w/wisemja01.html">James Wiseman</a></td><td class="left " data-stat="team_id"><a href="/contracts/DET.html">DET</a></td><td class="right salary-tm" data-stat="y1" csk="12119440">$12,119,440</td><td class="right iz" data-stat="y2"></td><td class="right iz" data-stat="y3"></td><td class="right iz" data-stat="y4"></td><td class="right iz" data-stat="y5"></td><td class="right iz" data-stat="y6"></td><td class="right " data-stat="remain_gtd" csk="12119440">$12,119,440</td></tr>        
            """
        ))
        self.assertEqual("James Wiseman", row.player_name)
        self.assertEqual("wisemja01", row.player_identifier)
        self.assertEqual("DET", row.team_abbreviation)
        self.assertEqual(("$12,119,440", "right salary-tm"), row.first_contract_year_data)
        self.assertEqual(("", "right iz"), row.second_contract_year_data)
        self.assertEqual(("", "right iz"), row.third_contract_year_data)
        self.assertEqual(("", "right iz"), row.fourth_contract_year_data)
        self.assertEqual(("", "right iz"), row.fifth_contract_year_data)
        self.assertEqual(("", "right iz"), row.sixth_contract_year_data)
        self.assertEqual("$12,119,440", row.guaranteed)
