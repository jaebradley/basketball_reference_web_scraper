from unittest import TestCase
from unittest.mock import MagicMock

from basketball_reference_web_scraper.html import PlayerPage, PlayerPageTotalsTable


class TestPlayerPage(TestCase):
    def test_name_is_none_when_no_name_headers(self):
        html = MagicMock()
        html.xpath = MagicMock(return_value=[])

        self.assertIsNone(PlayerPage(html=html).name)
        html.xpath.assert_called_once_with('.//h1[@itemprop="name"]')

    def test_name_is_first_name_header_content_when_name_headers(self):
        first_name_header = MagicMock()
        first_name_header.text_content = MagicMock(return_value="first name")

        second_name_header = MagicMock()
        second_name_header.text_content = MagicMock(return_value="second name")

        html = MagicMock()
        html.xpath = MagicMock(return_value=[first_name_header, second_name_header])

        self.assertEqual(
            PlayerPage(html=html).name,
            "first name"
        )
        html.xpath.assert_called_once_with('.//h1[@itemprop="name"]')

    def test_totals_table_is_none_when_no_totals_tables(self):
        html = MagicMock()
        html.xpath = MagicMock(return_value=[])

        self.assertIsNone(PlayerPage(html=html).totals_table)
        html.xpath.assert_called_once_with('.//table[@id="per_game"]')

    def test_totals_table_is_first_table_when_totals_tables(self):
        first_table = MagicMock()
        second_table = MagicMock()

        html = MagicMock()
        html.xpath = MagicMock(return_value=[first_table, second_table])

        self.assertEqual(
            PlayerPage(html=html).totals_table,
            PlayerPageTotalsTable(html=first_table),
        )
        html.xpath.assert_called_once_with('.//table[@id="per_game"]')
