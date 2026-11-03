"""Consumer workflows through the real client/parsers, using recorded HTML."""

import csv
import json
import subprocess
import sys
from pathlib import Path

import requests_mock

from basketball_reference_web_scraper.cli import main


FILES = Path(__file__).parent / "files"


def test_lookup_export_and_analyze_game_log(tmp_path, capsys):
    with requests_mock.Mocker() as upstream:
        upstream.get("https://www.basketball-reference.com/search/search.fcgi?search=Russell+Westbrook",
                     status_code=302, headers={"Location": "https://www.basketball-reference.com/players/w/westbru01.html"})
        # A direct player search redirect with a small player-page fixture.
        upstream.get("https://www.basketball-reference.com/players/w/westbru01.html", text='''
            <html><h1 itemprop="name"><span>Russell Westbrook</span></h1>
            <table id="per_game"><tbody><tr><td data-stat="lg_id">NBA</td></tr></tbody></table></html>''')
        upstream.get("https://www.basketball-reference.com/players/w/westbru01/gamelog/2019",
                     text=(FILES / "player_box_scores/2019/westbru01.html").read_text())
        assert main(["search", "Russell Westbrook"]) == 0
        result = json.loads(capsys.readouterr().out)
        identifier = result["players"][0]["identifier"]
        assert identifier == "westbru01"
        destination = tmp_path / "westbrook-2019.csv"
        assert main(["regular-season-player-box-scores", "--player", identifier,
                     "--season", "2019", "--format", "csv", "--output", str(destination)]) == 0
    assert capsys.readouterr().out == ""
    with destination.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    assert len(rows) == 73
    assert rows[0]["date"] == "2018-10-21"
    assert all(row["active"] == "True" for row in rows)
    average = sum(int(row["points_scored"]) for row in rows) / len(rows)
    assert round(average, 1) == 22.9


def test_recorded_contracts_are_serializable(capsys):
    with requests_mock.Mocker() as upstream:
        upstream.get("https://www.basketball-reference.com/contracts/players.html",
                     text=(FILES / "contracts/2025/03/07.html").read_text())
        assert main(["contracts"]) == 0
    contracts = json.loads(capsys.readouterr().out)
    assert len(contracts) > 100
    assert contracts[0]["player"]["identifier"]
    salaries = contracts[0]["salaries_by_season_start_year"].values()
    assert any(isinstance(salary["amount_in_usd"], str) for salary in salaries if salary)


def test_recorded_shooting_preserves_nested_fields(capsys):
    with requests_mock.Mocker() as upstream:
        upstream.get("https://www.basketball-reference.com/leagues/NBA_2025_shooting.html",
                     text=(FILES / "players_season_shooting_statistics/2025.html").read_text())
        assert main(["players-regular-season-shooting-statistics", "--season", "2025"]) == 0
    players = json.loads(capsys.readouterr().out)
    assert players[0]["two_point_shot_statistics"]["statistics_by_range"]["0-3"]["units"] == "feet"


def test_module_entrypoint_from_a_process():
    result = subprocess.run([sys.executable, "-m", "basketball_reference_web_scraper", "teams"],
                            capture_output=True, text=True, timeout=15, check=True)
    assert "BOSTON_CELTICS" in json.loads(result.stdout)
    assert result.stderr == ""
