import csv
import io
import json
from datetime import date
from decimal import Decimal
from unittest.mock import patch

import pytest
import requests

from basketball_reference_web_scraper import cli
from basketball_reference_web_scraper.contracts.data.models import (
    Contract,
    Player,
    Salary,
)
from basketball_reference_web_scraper.data import Team


@pytest.mark.parametrize(
    "command,arguments,expected",
    [
        ("search", [" LeBron James "], {"term": "LeBron James"}),
        ("standings", ["--season", "2019"], {"season_end_year": 2019}),
        (
            "player-box-scores",
            ["--date", "2018-01-01"],
            {"year": 2018, "month": 1, "day": 1},
        ),
        (
            "team-box-scores",
            ["--date", "2018-01-01"],
            {"year": 2018, "month": 1, "day": 1},
        ),
        (
            "regular-season-player-box-scores",
            ["--season", "2019", "--player", "jamesle01", "--include-inactive-games"],
            {
                "season_end_year": 2019,
                "player_identifier": "jamesle01",
                "include_inactive_games": True,
            },
        ),
        (
            "playoff-player-box-scores",
            ["--season", "2019", "--player", "jamesle01"],
            {
                "season_end_year": 2019,
                "player_identifier": "jamesle01",
                "include_inactive_games": False,
            },
        ),
        ("season-schedule", ["--season", "2019"], {"season_end_year": 2019}),
        ("players-season-totals", ["--season", "2019"], {"season_end_year": 2019}),
        (
            "players-advanced-season-totals",
            ["--season", "2019", "--include-combined-values"],
            {"season_end_year": 2019, "include_combined_values": True},
        ),
        (
            "players-regular-season-shooting-statistics",
            ["--season", "2019"],
            {"season_end_year": 2019},
        ),
        (
            "roster",
            ["--season", "2019", "--team", "Boston Celtics"],
            {"season_end_year": 2019, "team": Team.BOSTON_CELTICS},
        ),
        (
            "play-by-play",
            ["--date", "2018-01-01", "--home-team", "BOSTON_CELTICS"],
            {"year": 2018, "month": 1, "day": 1, "home_team": Team.BOSTON_CELTICS},
        ),
    ],
)
def test_dispatch(command, arguments, expected, capsys):
    function = cli.OPERATIONS[command][0]
    with patch.object(cli.client, function, return_value=[]) as fetch:
        assert cli.main([command, *arguments]) == 0
    fetch.assert_called_once_with(**expected)
    output = capsys.readouterr()
    assert json.loads(output.out) == []
    assert output.err == ""


def test_contracts_preserve_nested_data_and_exact_salary(capsys):
    contract = Contract(
        Player("jamesle01", "LeBron James"),
        Team.LOS_ANGELES_LAKERS,
        {2025: Salary(Decimal("52627153.01")), 2026: None},
        None,
    )

    def fetch(contract_processor):
        contract_processor(contract)

    with patch.object(cli.client, "contracts", side_effect=fetch):
        assert cli.main(["contracts"]) == 0
    record = json.loads(capsys.readouterr().out)[0]
    assert record["player"]["identifier"] == "jamesle01"
    assert record["team"] == "LOS ANGELES LAKERS"
    assert record["salaries_by_season_start_year"] == {
        "2025": {"amount_in_usd": "52627153.01"},
        "2026": None,
    }


@pytest.mark.parametrize("team", list(Team))
def test_every_team_key_and_full_name_can_be_used_in_a_task(team, capsys):
    for name in [team.name, "  " + team.value.lower() + "  "]:
        with patch.object(cli.client, "roster", return_value=[]) as fetch:
            assert cli.main(["roster", "--season", "1970", "--team", name]) == 0
        fetch.assert_called_once_with(team=team, season_end_year=1970)
        assert json.loads(capsys.readouterr().out) == []


@pytest.mark.parametrize(
    "arguments",
    [
        [],
        ["unknown"],
        ["standings"],
        ["search", "  "],
        ["standings", "--season", "2018-19"],
        ["standings", "--season", "10000"],
        ["standings", "--season", "0"],
        ["player-box-scores", "--date", "2019-02-29"],
        ["player-box-scores", "--date", "20180101"],
        [
            "regular-season-player-box-scores",
            "--season",
            "2019",
            "--player",
            "../secret",
        ],
        ["roster", "--season", "2019", "--team", "BOS"],
        ["contracts", "--format", "csv"],
        [
            "players-regular-season-shooting-statistics",
            "--season",
            "2019",
            "--format",
            "csv",
        ],
        ["standings", "--season", "2019", "--overwrite"],
    ],
)
def test_invalid_inputs_fail_before_network(arguments, capsys):
    with patch("requests.get") as fetch, pytest.raises(SystemExit) as stopped:
        cli.main(arguments)
    assert stopped.value.code == 2
    fetch.assert_not_called()
    output = capsys.readouterr()
    assert output.out == ""
    assert json.loads(output.err)["error"]["type"] == "invalid_arguments"


@pytest.mark.parametrize("status", [403, 404, 429, 503])
def test_http_failures_do_not_publish_or_replace_output(status, tmp_path, capsys):
    destination = tmp_path / "result.json"
    destination.write_text("original")
    response = requests.Response()
    response.status_code = status
    failure = requests.HTTPError("upstream failed", response=response)
    with patch.object(cli.client, "standings", side_effect=failure):
        assert (
            cli.main(
                [
                    "standings",
                    "--season",
                    "2019",
                    "--output",
                    str(destination),
                    "--overwrite",
                ]
            )
            == 1
        )
    assert destination.read_text() == "original"
    assert list(tmp_path.iterdir()) == [destination]
    output = capsys.readouterr()
    assert output.out == ""
    error = json.loads(output.err)["error"]
    assert error["type"] == "http_error"
    assert error["status_code"] == status


@pytest.mark.parametrize(
    "failure,kind",
    [
        (requests.Timeout("deadline"), "network_error"),
        (requests.ConnectionError("offline"), "network_error"),
        (ValueError("page structure changed"), "scrape_error"),
    ],
)
def test_runtime_failures_are_machine_readable(failure, kind, capsys):
    with patch.object(cli.client, "standings", side_effect=failure):
        assert cli.main(["standings", "--season", "2019"]) == 1
    output = capsys.readouterr()
    assert output.out == ""
    assert json.loads(output.err)["error"]["type"] == kind


def test_existing_file_and_missing_directory_fail_before_fetch(tmp_path, capsys):
    existing = tmp_path / "data.json"
    existing.write_text("keep")
    for destination in [existing, tmp_path / "missing" / "data.json"]:
        with patch.object(cli.client, "standings") as fetch:
            assert (
                cli.main(
                    ["standings", "--season", "2019", "--output", str(destination)]
                )
                == 1
            )
        fetch.assert_not_called()
        assert json.loads(capsys.readouterr().err)["error"]["type"] == "output_error"
    assert existing.read_text() == "keep"


def test_json_handles_dates_enums_sets_and_unicode(capsys):
    row = {
        "date": date(2019, 1, 1),
        "team": Team.BOSTON_CELTICS,
        "tags": {"NBA"},
        "name": "Nikola Jokić",
    }
    with patch.object(cli.client, "standings", return_value=[row]):
        assert cli.main(["standings", "--season", "2019"]) == 0
    assert json.loads(capsys.readouterr().out) == [
        {
            "date": "2019-01-01",
            "team": "BOSTON CELTICS",
            "tags": ["NBA"],
            "name": "Nikola Jokić",
        }
    ]


def test_csv_stdout_quotes_search_and_has_header_when_empty(capsys):
    player = {"name": 'Name, "Quoted"', "identifier": "quoted01"}
    with patch.object(cli.client, "search", return_value={"players": [player]}):
        assert cli.main(["search", "Quoted", "--format", "csv"]) == 0
    rows = list(csv.DictReader(io.StringIO(capsys.readouterr().out)))
    assert rows[0]["name"] == player["name"]
    with patch.object(cli.client, "search", return_value={"players": []}):
        assert cli.main(["search", "Unknown", "--format", "csv"]) == 0
    output = capsys.readouterr().out
    assert list(csv.DictReader(io.StringIO(output))) == []
    assert "identifier" in output


def test_file_publication_and_explicit_overwrite(tmp_path, capsys):
    destination = tmp_path / "résult.json"
    for data, extra in [([], []), ([{"name": "Jokić"}], ["--overwrite"])]:
        with patch.object(cli.client, "standings", return_value=data):
            assert (
                cli.main(
                    [
                        "standings",
                        "--season",
                        "2019",
                        "--output",
                        str(destination),
                        *extra,
                    ]
                )
                == 0
            )
        assert json.loads(destination.read_text(encoding="utf-8")) == data
        assert capsys.readouterr().out == ""
    assert list(tmp_path.iterdir()) == [destination]


def test_publication_race_preserves_other_writer(tmp_path):
    destination = tmp_path / "result.json"
    original_link = cli.os.link

    def competing_writer(source, target):
        destination.write_text("other writer")
        original_link(source, target)

    with (
        patch.object(cli.os, "link", side_effect=competing_writer),
        pytest.raises(FileExistsError),
    ):
        cli._write_file(destination, "our result", overwrite=False)
    assert destination.read_text() == "other writer"
    assert list(tmp_path.iterdir()) == [destination]


def test_serialization_failure_preserves_file(tmp_path, capsys):
    destination = tmp_path / "result.json"
    destination.write_text("keep")
    with patch.object(cli.client, "standings", return_value=[{"value": float("nan")}]):
        assert (
            cli.main(
                [
                    "standings",
                    "--season",
                    "2019",
                    "--output",
                    str(destination),
                    "--overwrite",
                ]
            )
            == 1
        )
    assert destination.read_text() == "keep"
    assert json.loads(capsys.readouterr().err)["error"]["type"] == "scrape_error"


def test_help_and_team_discovery_are_offline(capsys):
    with patch("requests.get") as fetch:
        assert cli.main(["teams"]) == 0
        assert "BOSTON_CELTICS" in json.loads(capsys.readouterr().out)
        with pytest.raises(SystemExit) as stopped:
            cli.main(["--help"])
        assert stopped.value.code == 0
        assert "playoff-player-box-scores" in capsys.readouterr().out
    fetch.assert_not_called()
