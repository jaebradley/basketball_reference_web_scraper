import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from basketball_reference_web_scraper import cli, client, diagnostics
from basketball_reference_web_scraper.http_service import HTTPService

SCHEDULE_PAGE = (
    '<html><body><div id="content">'
    '<div class="filter"><div class="current"><a>October</a></div>'
    '<div><a href="/leagues/NBA_2019_games-november.html">November</a></div></div>'
    '<table id="schedule"><tbody><tr>'
    '<th data-stat="date_game">Tue, Oct 30, 2018</th>'
    '<td data-stat="game_start_time">7:00p</td>'
    '<td data-stat="visitor_team_name">Boston Celtics</td>'
    '<td data-stat="visitor_pts">100</td>'
    '<td data-stat="home_team_name">Cleveland Cavaliers</td>'
    '<td data-stat="home_pts">99</td>'
    "</tr></tbody></table></div></body></html>"
).encode()

STANDINGS_PAGE = (
    '<html><body><div id="content">'
    '<table id="divs_standings_E"><tbody><tr>'
    '<th data-stat="team_name">Boston Celtics</th>'
    "</tr></tbody></table></div></body></html>"
).encode()

EMPTY_STANDINGS = (
    '<html><body><div id="content">'
    '<table id="divs_standings_E"><tbody></tbody></table>'
    "</div></body></html>"
).encode()


class StubServer(BaseHTTPRequestHandler):
    routes = {}

    def log_message(self, format, *args):  # noqa: A002
        pass

    def do_GET(self):
        import time

        entry = StubServer.routes.get(self.path)
        if entry is None:
            entry = (404, {}, b"not found")
        status, headers, body = entry
        if status == "stall":
            time.sleep(3)
            return
        if status == "truncated_stream":
            self.send_response(200)
            self.send_header("Content-Length", "1000")
            self.end_headers()
            self.wfile.write(body)
            self.close_connection = True
            return
        self.send_response(status)
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)


@pytest.fixture()
def stub_server(monkeypatch):
    server = ThreadingHTTPServer(("127.0.0.1", 0), StubServer)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    monkeypatch.setattr(
        HTTPService, "BASE_URL", f"http://127.0.0.1:{server.server_address[1]}"
    )
    yield server
    server.shutdown()
    server.server_close()


@pytest.fixture()
def journal(monkeypatch, tmp_path):
    directory = tmp_path / "diagnostics"
    directory.mkdir()
    monkeypatch.setenv("BASKETBALL_REFERENCE_DIAGNOSTICS", "on")
    monkeypatch.setenv("BASKETBALL_REFERENCE_DIAGNOSTICS_DIR", str(directory))
    diagnostics.reset()
    yield directory
    diagnostics.reset()


def journal_events(directory):
    events = []
    for path in sorted(directory.glob("*.jsonl")):
        events.extend(
            json.loads(line) for line in path.read_text().splitlines() if line
        )
    return events


def events_of_type(directory, event_type):
    return [e for e in journal_events(directory) if e.get("event") == event_type]


def test_failed_run_retains_retrievable_evidence(stub_server, journal, capsys):
    StubServer.routes = {"/leagues/NBA_2019.html": (503, {}, b"busy")}
    exit_code = cli.main(["standings", "--season", "2019"])
    assert exit_code == 1

    run_files = list(journal.glob("*.jsonl"))
    assert len(run_files) == 1  # One per run: evidence survives the process.

    starts = events_of_type(journal, "run_start")
    assert starts and starts[0]["environment"]["package_version"]
    assert starts[0]["environment"]["python"]

    requests_ = events_of_type(journal, "http_request")
    assert len(requests_) == 1
    failure = requests_[0]
    assert failure["operation"] == "standings"
    assert failure["method"] == "GET"
    assert failure["url"].endswith("/leagues/NBA_2019.html")
    assert failure["status"] == 503
    assert failure["outcome"] == "response"
    assert isinstance(failure["elapsed_ms"], float)
    assert failure["request_seq"] == 1
    assert failure["ts"].endswith("Z")

    ends = events_of_type(journal, "operation_end")
    assert ends[0]["outcome"] == "error"
    assert ends[0]["error"]["type"] == "HTTPError"
    assert ends[0]["last_url"].endswith("/leagues/NBA_2019.html")

    errors = events_of_type(journal, "error")
    assert errors[0]["kind"] == "http_error"
    assert errors[0]["status_code"] == 503

    run_ends = events_of_type(journal, "run_end")
    assert len(run_ends) == 1 and run_ends[0]["exit_code"] == 1

    stderr = json.loads(capsys.readouterr().err)
    assert stderr["error"]["type"] == "http_error"
    assert stderr["error"]["run_id"] == starts[0]["run_id"]
    assert stderr["error"]["diagnostics_path"] == str(run_files[0])


def test_timeout_records_attempt_and_elapsed(stub_server, journal, monkeypatch):
    monkeypatch.setattr(HTTPService, "DEFAULT_REQUEST_TIMEOUT_SECONDS", 1)
    StubServer.routes = {"/leagues/NBA_2019_totals.html": ("stall", {}, b"")}
    assert cli.main(["players-season-totals", "--season", "2019"]) == 1
    failure = events_of_type(journal, "http_request")[0]
    assert failure["outcome"] == "timeout"
    assert failure["error"] == "ReadTimeout"
    assert failure["url"].endswith("/leagues/NBA_2019_totals.html")
    assert failure["elapsed_ms"] >= 0


def test_rate_limit_records_retry_after(stub_server, journal):
    StubServer.routes = {
        "/search/search.fcgi?search=Russell+Westbrook": (
            429,
            {"Retry-After": "60"},
            b"slow down",
        )
    }
    assert cli.main(["search", "Russell Westbrook"]) == 1
    limited = events_of_type(journal, "http_request")[0]
    assert limited["status"] == 429
    assert limited["retry_after"] == "60"


def test_sibling_fetches_are_recorded_when_one_fails(stub_server, journal):
    StubServer.routes = {
        "/leagues/NBA_2019_games.html": (200, {}, SCHEDULE_PAGE),
        "/leagues/NBA_2019_games-november.html": (500, {}, b""),
    }
    assert cli.main(["season-schedule", "--season", "2019"]) == 1
    outcomes = [
        (event["url"].rsplit("/", 1)[-1], event["status"])
        for event in events_of_type(journal, "http_request")
    ]
    # Both sibling pages are in the evidence even though the run raised.
    assert ("NBA_2019_games.html", 200) in outcomes
    assert ("NBA_2019_games-november.html", 500) in outcomes


def test_structure_drift_error_records_page_context(stub_server, journal, capsys):
    StubServer.routes = {"/leagues/NBA_2019.html": (200, {}, EMPTY_STANDINGS)}
    assert cli.main(["standings", "--season", "2019"]) == 1
    ends = events_of_type(journal, "operation_end")
    assert ends[0]["outcome"] == "error"
    assert "AttributeError" in ends[0]["error"]["traceback"]
    assert ends[0]["last_url"].endswith("/leagues/NBA_2019.html")
    stderr = json.loads(capsys.readouterr().err)
    assert stderr["error"]["type"] == "scrape_error"
    assert stderr["error"]["run_id"]


OCTOBER_ONLY_SCHEDULE = SCHEDULE_PAGE.replace(
    b'<div><a href="/leagues/NBA_2019_games-november.html">November</a></div>', b""
)


def test_operations_share_run_id_across_invocations(stub_server, journal):
    StubServer.routes = {
        "/leagues/NBA_2019_games.html": (200, {}, OCTOBER_ONLY_SCHEDULE)
    }
    assert cli.main(["season-schedule", "--season", "2019"]) == 0
    assert cli.main(["season-schedule", "--season", "2019"]) == 0
    starts = events_of_type(journal, "operation_start")
    assert len(starts) == 2
    assert len({start["run_id"] for start in starts}) == 1
    assert [start["operation"] for start in starts] == [
        "season_schedule",
        "season_schedule",
    ]


def test_empty_success_records_row_count(stub_server, journal):
    StubServer.routes = {
        "/leagues/NBA_2019_games.html": (200, {}, OCTOBER_ONLY_SCHEDULE)
    }
    assert cli.main(["season-schedule", "--season", "2019", "--format", "csv"]) == 0
    ok_endings = [
        event
        for event in events_of_type(journal, "operation_end")
        if event["outcome"] == "ok"
    ]
    assert ok_endings and ok_endings[0]["row_count"] == 1
    assert events_of_type(journal, "run_end")[0]["exit_code"] == 0


def test_telemetry_failure_does_not_change_behavior(
    monkeypatch, tmp_path, stub_server, capsys
):
    # The configured "directory" is a file: journaling cannot be initialized.
    blocker = tmp_path / "blocker"
    blocker.write_text("not a directory")
    monkeypatch.setenv("BASKETBALL_REFERENCE_DIAGNOSTICS", "on")
    monkeypatch.setenv("BASKETBALL_REFERENCE_DIAGNOSTICS_DIR", str(blocker))
    diagnostics.reset()
    StubServer.routes = {"/leagues/NBA_2019.html": (503, {}, b"busy")}
    assert cli.main(["standings", "--season", "2019"]) == 1
    stderr = json.loads(capsys.readouterr().err)
    assert stderr["error"]["type"] == "http_error"
    assert stderr["error"]["status_code"] == 503
    diagnostics.reset()


def test_retention_prunes_oldest_runs(journal):
    for index in range(diagnostics.MAX_JOURNAL_FILES + 4):
        stale = journal / f"20200101T0000{index:02d}Z-{index:012d}.jsonl"
        stale.write_text("")
    diagnostics.start_run()
    remaining = sorted(journal.glob("*.jsonl"))
    assert len(remaining) == diagnostics.MAX_JOURNAL_FILES
    assert "20200101T000000Z-000000000000.jsonl" not in {
        path.name for path in remaining
    }


def test_journal_size_cap_stops_writing(journal, monkeypatch):
    monkeypatch.setattr(diagnostics, "MAX_JOURNAL_BYTES", 600)
    run = diagnostics.start_run()
    for _ in range(50):
        diagnostics.record_error("http_error", "x" * 200)
    text = run.path.read_text()
    assert "journal_limit" in text
    assert len(text.splitlines()) < 50


def test_query_filters_by_operation_event_and_time(journal, stub_server, capsys):
    StubServer.routes = {
        "/leagues/NBA_2019_games.html": (200, {}, OCTOBER_ONLY_SCHEDULE)
    }
    cli.main(["season-schedule", "--season", "2019"])
    capsys.readouterr()  # Discard the scrape run's own output.
    run_id = events_of_type(journal, "run_start")[0]["run_id"]

    assert (
        cli.main(
            [
                "diagnostics",
                "--dir",
                str(journal),
                "--operation",
                "season_schedule",
                "--event",
                "http_request",
            ]
        )
        == 0
    )
    listed = json.loads(capsys.readouterr().out)
    assert len(listed) == 1 and listed[0]["status"] == 200

    assert cli.main(["diagnostics", "--dir", str(journal), "--run-id", run_id]) == 0
    assert json.loads(capsys.readouterr().out)

    assert (
        cli.main(
            ["diagnostics", "--dir", str(journal), "--since", "2099-01-01T00:00:00Z"]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out) == []

    assert cli.main(["diagnostics", "--dir", str(journal), "--runs"]) == 0
    summary = json.loads(capsys.readouterr().out)[0]
    assert summary["run_id"] == run_id
    assert summary["exit_code"] == 0

    assert (
        cli.main(["diagnostics", "--dir", str(journal), "--since", "not-a-date"]) == 2
    )
    assert json.loads(capsys.readouterr().err)["error"]["type"] == "invalid_arguments"


def test_read_events_ignores_torn_lines(journal):
    run = diagnostics.start_run()
    diagnostics.record_error("http_error", "boom")
    with open(run.path, "a", encoding="utf-8") as handle:
        handle.write('{"ts": "torn", "run_i')
    events = diagnostics.read_events(directory=journal)
    assert [event["event"] for event in events] == ["error", "run_start"]


def test_disabled_diagnostics_writes_nothing(tmp_path, monkeypatch):
    directory = tmp_path / "journal"
    monkeypatch.setenv("BASKETBALL_REFERENCE_DIAGNOSTICS", "off")
    monkeypatch.setenv("BASKETBALL_REFERENCE_DIAGNOSTICS_DIR", str(directory))
    diagnostics.reset()
    assert cli.main(["teams"]) == 0
    assert diagnostics.current_run_id() is None
    assert list(directory.glob("*.jsonl")) == []


def test_recorded_values_are_bounded(journal, stub_server):
    long_term = "x" * 500
    StubServer.routes = {
        f"/search/search.fcgi?search={long_term}": (200, {}, b"<html></html>")
    }
    cli.main(["search", long_term])  # Parse outcome is irrelevant to the evidence.
    events = events_of_type(journal, "http_request")
    recorded_term = events[0]["params"]["search"]
    assert len(recorded_term) <= diagnostics.MAX_FIELD_CHARS + len("…[truncated]")


def test_package_version_falls_back_to_unknown(monkeypatch):
    from importlib.metadata import PackageNotFoundError

    def raise_not_found(name):
        raise PackageNotFoundError(name)

    monkeypatch.setattr(diagnostics, "_importlib_version", raise_not_found)
    assert diagnostics.package_version() == "unknown"


def test_interrupted_contract_stream_is_distinguishable(stub_server, journal):
    partial = b'<html><body><table id="contracts">' + b"x" * 20
    StubServer.routes = {"/contracts/players.html": ("truncated_stream", {}, partial)}

    received = []
    with pytest.raises(Exception):
        client.contracts(contract_processor=received.append)

    streams = events_of_type(journal, "http_stream")
    assert streams and streams[0]["outcome"] == "interrupted"
    assert streams[0]["error"] == "ChunkedEncodingError"
    assert isinstance(streams[0]["stream_chars"], int)
    assert streams[0]["url"].endswith("/contracts/players.html")


def test_invalid_arguments_are_journalled(journal, capsys):
    with pytest.raises(SystemExit) as exit_request:
        cli.main(["standings", "--season", "not-a-year"])
    assert exit_request.value.code == 2

    stderr = json.loads(capsys.readouterr().err.strip())
    assert stderr["error"]["type"] == "invalid_arguments"
    assert stderr["error"]["run_id"]
    assert stderr["error"]["diagnostics_path"]

    errors = events_of_type(journal, "error")
    assert errors and errors[0]["kind"] == "invalid_arguments"
    assert errors[0]["message"].startswith("argument --season")

    ends = events_of_type(journal, "run_end")
    assert ends and ends[0]["exit_code"] == 2


def test_overwrite_without_output_is_journalled(journal, capsys):
    with pytest.raises(SystemExit) as exit_request:
        cli.main(["standings", "--season", "2019", "--overwrite"])
    assert exit_request.value.code == 2

    stderr = json.loads(capsys.readouterr().err.strip())
    assert stderr["error"]["type"] == "invalid_arguments"

    ends = events_of_type(journal, "run_end")
    assert ends and ends[0]["exit_code"] == 2
