from unittest import TestCase
from unittest.mock import patch, MagicMock, PropertyMock

from basketball_reference_web_scraper.html import SearchPage, PlayerSearchResult


class TestSearchPage(TestCase):
    def test_nba_aba_baa_players_content_query(self):
        self.assertEqual(
            SearchPage(html=MagicMock()).nba_aba_baa_players_content_query,
            '//div[@id="searches"]/div[@id="players"]',
        )

    @patch.object(SearchPage, 'nba_aba_baa_players_content_query', new_callable=PropertyMock)
    def test_nba_aba_baa_players_pagination_links_query(self, mocked_query):
        mocked_query.return_value = "some query"

        self.assertEqual(
            SearchPage(html=MagicMock()).nba_aba_baa_players_pagination_links_query,
            'some query/div[@class="search-pagination"]/a',
        )

    @patch.object(SearchPage, 'nba_aba_baa_players_content_query', new_callable=PropertyMock)
    def test_nba_aba_baa_player_search_items_query(self, mocked_query):
        mocked_query.return_value = "some query"

        self.assertEqual(
            SearchPage(html=MagicMock()).nba_aba_baa_player_search_items_query,
            'some query/div[@class="search-item"]',
        )

    @patch.object(SearchPage, 'nba_aba_baa_players_pagination_links_query', new_callable=PropertyMock)
    def test_nba_aba_baa_players_pagination_links(self, mocked_query):
        mocked_query.return_value = "some query"
        html = MagicMock()
        links = [MagicMock(return_value="some"), MagicMock(return_value="links")]
        html.xpath = MagicMock(return_value=links)

        self.assertEqual(
            SearchPage(html=html).nba_aba_baa_players_pagination_links,
            links,
        )
        html.xpath.asset_called_once_with("some query")

    @patch.object(SearchPage, 'nba_aba_baa_players_pagination_links', new_callable=PropertyMock)
    def test_nba_aba_baa_players_pagination_url_is_none_when_no_pagination_links(self, mocked_links):
        mocked_links.return_value = []
        self.assertIsNone(SearchPage(html=MagicMock()).nba_aba_baa_players_pagination_url)

    @patch.object(SearchPage, 'nba_aba_baa_players_pagination_links', new_callable=PropertyMock)
    def test_nba_aba_baa_players_pagination_url_is_first_link_href_attrib_when_single_link_is_not_at_end_of_results(
            self,
            mocked_links
    ):
        link = MagicMock()
        link.text_content = MagicMock(return_value="jaebaebae")
        link.attrib = MagicMock()
        link.attrib.__getitem__ = MagicMock(return_value="some text content")
        mocked_links.return_value = [link]

        self.assertEqual(
            SearchPage(html=MagicMock()).nba_aba_baa_players_pagination_url,
            "some text content",
        )
        link.attrib.__getitem__.assert_called_once_with("href")

    @patch.object(SearchPage, 'nba_aba_baa_players_pagination_links', new_callable=PropertyMock)
    def test_nba_aba_baa_players_pagination_url_is_none_when_single_link_is_at_end_of_results(
            self,
            mocked_links
    ):
        link = MagicMock()
        link.text_content = MagicMock(return_value="Previous 100 Results")
        mocked_links.return_value = [link]

        self.assertIsNone(SearchPage(html=MagicMock()).nba_aba_baa_players_pagination_url)
        link.text_content.assert_called_once_with()

    @patch.object(SearchPage, 'nba_aba_baa_players_pagination_links', new_callable=PropertyMock)
    def test_nba_aba_baa_players_pagination_url_is_second_link_href_attrib_when_multiple_links(
            self,
            mocked_links
    ):
        first_link = MagicMock()
        first_link.attrib = MagicMock()
        first_link.attrib.__getitem__ = MagicMock(return_value="some text content")

        second_link = MagicMock()
        second_link.attrib = MagicMock()
        second_link.attrib.__getitem__ = MagicMock(return_value="some other text content")
        mocked_links.return_value = [first_link, second_link]

        self.assertEqual(
            SearchPage(html=MagicMock()).nba_aba_baa_players_pagination_url,
            "some other text content",
        )
        second_link.attrib.__getitem__.assert_called_once_with("href")

    @patch.object(SearchPage, 'nba_aba_baa_player_search_items_query', new_callable=PropertyMock)
    def test_nba_aba_baa_players(self, mocked_query):
        mocked_query.return_value = "some query"

        first_result = MagicMock(name="first html result")
        second_result = MagicMock(name="second html result")
        third_result = MagicMock(name="third html result")

        html = MagicMock()
        html.xpath = MagicMock(return_value=[first_result, second_result, third_result])

        self.assertEqual(
            SearchPage(html=html).nba_aba_baa_players,
            [
                PlayerSearchResult(html=first_result),
                PlayerSearchResult(html=second_result),
                PlayerSearchResult(html=third_result),
            ]
        )
