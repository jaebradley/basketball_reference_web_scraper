from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from basketball_reference_web_scraper.html import SchedulePage, ScheduleRow


class TestSchedulePage(TestCase):
    def setUp(self):
        self.html = MagicMock()

    def test_other_months_schedule_links_query(self):
        self.assertEqual(
            SchedulePage(html=self.html).other_months_schedule_links_query,
            '//div[@id="content"]/div[@class="filter"]/div[not(contains(@class, "current"))]/a'
        )

    def test_rows_query(self):
        self.assertEqual(
            SchedulePage(html=self.html).rows_query,
            '//table[@id="schedule"]//tbody/tr'
        )

    @patch.object(SchedulePage, 'other_months_schedule_links_query', new_callable=PropertyMock)
    def test_other_months_schedule_urls(self, mocked_other_months_schedule_links_query):
        query = "some query"
        mocked_other_months_schedule_links_query.return_value = query
        link_href = "some link href"
        link = MagicMock()
        link.attrib = MagicMock()
        link.attrib.__getitem__ = MagicMock(return_value=link_href)
        links = [link]
        self.html.xpath = MagicMock(return_value=links)

        self.assertEqual(
            SchedulePage(html=self.html).other_months_schedule_urls,
            [link_href]
        )
        self.html.xpath.assert_called_once_with(query)
        link.attrib.__getitem__.assert_called_once_with('href')

    @patch.object(SchedulePage, 'rows_query', new_callable=PropertyMock)
    def test_no_rows_are_returned_when_all_rows_have_playoffs_content(self, mocked_rows_query):
        query = "some query"
        mocked_rows_query.return_value = query
        playoff_row = MagicMock()
        playoff_row.text_content = MagicMock(return_value="Playoffs")
        rows = [playoff_row]
        self.html.xpath = MagicMock(return_value=rows)

        self.assertEqual(
            SchedulePage(html=self.html).rows,
            []
        )
        self.html.xpath.assert_called_once_with(query)
        playoff_row.text_content.assert_called_once_with()

    @patch.object(SchedulePage, 'rows_query', new_callable=PropertyMock)
    def test_all_rows_are_returned_when_all_rows_have_playoffs_content(self, mocked_rows_query):
        query = "some query"
        mocked_rows_query.return_value = query
        non_playoff_row = MagicMock()
        non_playoff_row.text_content = MagicMock(return_value="jaebaebae")
        rows = [non_playoff_row]
        self.html.xpath = MagicMock(return_value=rows)

        self.assertEqual(
            SchedulePage(html=self.html).rows,
            [
                ScheduleRow(html=non_playoff_row)
            ]
        )
