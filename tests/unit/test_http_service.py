import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest import TestCase, mock

from requests import codes

from basketball_reference_web_scraper.errors import InvalidDate
from basketball_reference_web_scraper.http_service import HTTPService, _default_session
from basketball_reference_web_scraper.parser_service import ParserService


def _page(rows, other_months=""):
    return (
        '<html><body><div id="content">'
        '<div class="filter"><div class="current"><a>October</a></div>'
        f"{other_months}</div>"
        '<table id="schedule"><tbody>'
        f"{rows}"
        "</tbody></table></div></body></html>"
    )


def _row(date, away, home, away_score=100, home_score=99):
    return (
        "<tr>"
        f'<th data-stat="date_game">{date}</th>'
        '<td data-stat="game_start_time">7:00p</td>'
        f'<td data-stat="visitor_team_name">{away}</td>'
        f'<td data-stat="visitor_pts">{away_score}</td>'
        f'<td data-stat="home_team_name">{home}</td>'
        f'<td data-stat="home_pts">{home_score}</td>'
        "</tr>"
    )


class _FakeResponse:
    def __init__(self, body):
        self.content = body.encode()
        self.status_code = codes.ok

    def raise_for_status(self):
        pass


class TestHTTPService(TestCase):
    @mock.patch("requests.Session.get")
    def test_player_box_scores_raises_invalid_date_for_300_response(self, mocked_get):
        response = mock.Mock(status_code=codes.multiple_choices)
        mocked_get.return_value = response
        self.assertRaisesRegex(
            InvalidDate,
            "Date with year set to 2018, month set to 1, and day set to 1 is invalid",
            HTTPService(parser=mock.MagicMock()).player_box_scores,
            day=1,
            month=1,
            year=2018,
        )

    def test_schedule_month_pages_are_fetched_concurrently_and_keep_order(self):
        pages = {
            "games-november.html": _page(
                _row("Thu, Nov 1, 2018", "Boston Celtics", "Cleveland Cavaliers")
            ),
            "games-december.html": _page(
                _row("Sat, Dec 1, 2018", "Golden State Warriors", "Los Angeles Lakers")
            ),
        }
        barrier = threading.Barrier(2)

        class FakeSession:
            def get(self, url, **kwargs):
                for suffix, body in pages.items():
                    if url.endswith(suffix):
                        barrier.wait(timeout=5)
                        return _FakeResponse(body)
                return _FakeResponse(
                    _page(
                        _row(
                            "Tue, Oct 30, 2018", "Boston Celtics", "Cleveland Cavaliers"
                        ),
                        '<div><a href="/leagues/NBA_2019_games-november.html">November</a></div>'
                        '<div><a href="/leagues/NBA_2019_games-december.html">December</a></div>',
                    )
                )

        service = HTTPService(parser=ParserService(), session_factory=FakeSession)
        rows = service.season_schedule(2019, max_workers=2)
        self.assertEqual(
            [row["date"].isoformat() for row in rows],
            ["2018-10-30", "2018-11-01", "2018-12-01"],
        )

    def test_sequential_requests_reuse_one_connection(self):
        ports = []

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_GET(self):
                ports.append(self.client_address[1])
                body = _page(
                    _row("Tue, Oct 17, 2017", "Boston Celtics", "Cleveland Cavaliers")
                ).encode()
                self.send_response(codes.ok)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            _default_session().trust_env = False
            url = f"http://127.0.0.1:{server.server_port}/schedule"
            # A fresh service per request mirrors one client call per player.
            for _ in range(3):
                HTTPService(parser=ParserService()).schedule_for_month(url)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
        self.assertEqual(len(ports), 3)
        self.assertEqual(len(set(ports)), 1)

    def test_custom_session_factories_are_isolated_per_service(self):
        class FirstSession:
            pass

        class SecondSession:
            pass

        first = HTTPService(parser=ParserService(), session_factory=FirstSession)
        second = HTTPService(parser=ParserService(), session_factory=SecondSession)
        self.assertIsInstance(first.session, FirstSession)
        self.assertIsInstance(second.session, SecondSession)
        self.assertIsNot(first.session, second.session)
