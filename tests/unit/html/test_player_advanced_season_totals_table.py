from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock
from unittest.mock import patch

from basketball_reference_web_scraper.html import PlayerAdvancedSeasonTotalsRow, PlayerAdvancedSeasonTotalsTable


class TestPlayerAdvancedSeasonTotalsTable(TestCase):
    def setUp(self):
        self.html = MagicMock()

    def test_rows_query_after_stripping_whitespace(self):
        self.assertEqual(
            """
            //table[@id="advanced_stats"]
            /tbody
            /tr[
                contains(@class, "full_table") or 
                contains(@class, "italic_text partial_table") 
                and not(contains(@class, "rowSum"))
            ]
            """.strip(),
            PlayerAdvancedSeasonTotalsTable(html=self.html).rows_query.strip(),
        )

    @patch.object(PlayerAdvancedSeasonTotalsRow, 'is_combined_totals', new_callable=PropertyMock, return_value=False)
    def test_returns_all_rows_when_rows_are_not_combined_totals_rows(self, _):
        first_html_row = MagicMock()
        html_rows = [first_html_row]
        self.html.xpath = MagicMock(return_value=html_rows)

        rows = PlayerAdvancedSeasonTotalsTable(self.html).get_rows()
        self.assertTrue(len(html_rows) == len(rows))

    @patch.object(PlayerAdvancedSeasonTotalsRow, 'is_combined_totals', new_callable=PropertyMock, return_value=True)
    def test_returns_no_rows_when_all_rows_are_combined_totals_rows(self, _):
        first_html_row = MagicMock()
        html_rows = [first_html_row]
        self.html.xpath = MagicMock(return_value=html_rows)

        rows = PlayerAdvancedSeasonTotalsTable(self.html).get_rows()
        self.assertTrue(0 == len(rows))

