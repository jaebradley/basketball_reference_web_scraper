import requests_mock
from unittest import TestCase

from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.http_service import HTTPService

BASE_URL = "https://www.basketball-reference.com"

SEARCH_ITEM_HTML = (
    '<div class="search-item">'
    '<div class="search-item-name"><a href="/players/b/bryanko01k.html">Kobe Bryant</a></div>'
    '<div class="search-item-league">NBA</div>'
    "</div>"
)


class TestSearch(TestCase):
    @requests_mock.Mocker()
    def test_requests_include_timeout(self, m):
        m.get(
            f"{BASE_URL}/search/search.fcgi?search=kobe",
            text=f'<html><body><div id="searches"><div id="players">{SEARCH_ITEM_HTML}</div></div></body></html>',
        )

        client.search(term="kobe")

        self.assertEqual(1, len(m.request_history))
        self.assertEqual(
            HTTPService.DEFAULT_REQUEST_TIMEOUT_SECONDS, m.request_history[0].timeout
        )

    @requests_mock.Mocker()
    def test_self_referential_pagination_does_not_loop_forever(self, m):
        self_referential_html = (
            f'<html><body><div id="searches"><div id="players">{SEARCH_ITEM_HTML}'
            '<div class="search-pagination">'
            '<a href="search.fcgi?search=kobe&amp;idx=100">Next 100 Results</a>'
            "</div></div></body></html>"
        )
        m.get(f"{BASE_URL}/search/search.fcgi?search=kobe", text=self_referential_html)
        m.get(
            f"{BASE_URL}/search/search.fcgi?search=kobe&idx=100",
            text=self_referential_html,
        )

        results = client.search(term="kobe")

        self.assertEqual(2, len(results["players"]))
        self.assertEqual(2, len(m.request_history))

    @requests_mock.Mocker()
    def test_pagination_with_absolute_path_href_results_in_valid_url(self, m):
        paginated_html = (
            f'<html><body><div id="searches"><div id="players">{SEARCH_ITEM_HTML}'
            '<div class="search-pagination">'
            '<a href="/search/search.fcgi?search=kobe&amp;idx=100">Next 100 Results</a>'
            "</div></div></body></html>"
        )
        m.get(f"{BASE_URL}/search/search.fcgi?search=kobe", text=paginated_html)
        m.get(
            f"{BASE_URL}/search/search.fcgi?search=kobe&idx=100",
            text=f'<html><body><div id="searches"><div id="players">{SEARCH_ITEM_HTML}</div></div></body></html>',
        )

        results = client.search(term="kobe")

        self.assertEqual(2, len(results["players"]))
        self.assertEqual(
            f"{BASE_URL}/search/search.fcgi?search=kobe&idx=100",
            m.request_history[1].url,
        )
