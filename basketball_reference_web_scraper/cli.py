"""Shell interface for agents and command-line consumers of the Python client."""

import argparse
import csv
import io
import json
import os
import re
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, is_dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path

import requests

from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.errors import (
    CouldNotGetPlayerContractData,
    InvalidDate,
    InvalidPlayerAndSeason,
    InvalidSeason,
    InvalidTeamSeason,
)
from basketball_reference_web_scraper.output import columns
from basketball_reference_web_scraper.output.fields import (
    BasketballReferenceJSONEncoder,
    format_value,
)


# Public client function, task description, and the existing CSV schema.
OPERATIONS = {
    "search": (
        "search",
        "Find player identifiers by name",
        columns.SEARCH_RESULTS_COLUMN_NAMES,
    ),
    "standings": (
        "standings",
        "Division standings for a season",
        columns.STANDINGS_COLUMNS_NAMES,
    ),
    "player-box-scores": (
        "player_box_scores",
        "Player box scores on a date",
        columns.BOX_SCORE_COLUMN_NAMES,
    ),
    "team-box-scores": (
        "team_box_scores",
        "Team box scores on a date",
        columns.TEAM_BOX_SCORES_COLUMN_NAMES,
    ),
    "regular-season-player-box-scores": (
        "regular_season_player_box_scores",
        "Regular-season game logs; repeat --player to combine players",
        columns.PLAYER_SEASON_BOX_SCORE_COLUMN_NAMES,
    ),
    "playoff-player-box-scores": (
        "playoff_player_box_scores",
        "Playoff game logs; repeat --player to combine players",
        columns.PLAYER_SEASON_BOX_SCORE_COLUMN_NAMES,
    ),
    "season-schedule": (
        "season_schedule",
        "All scheduled games for one or more seasons",
        columns.SCHEDULE_COLUMN_NAMES,
    ),
    "players-season-totals": (
        "players_season_totals",
        "All players' regular-season totals",
        columns.PLAYER_SEASON_TOTALS_COLUMN_NAMES,
    ),
    "players-advanced-season-totals": (
        "players_advanced_season_totals",
        "All players' advanced regular-season statistics",
        columns.PLAYER_ADVANCED_SEASON_TOTALS_COLUMN_NAMES,
    ),
    "players-regular-season-shooting-statistics": (
        "players_regular_season_shooting_statistics",
        "Nested shooting statistics (JSON only)",
        None,
    ),
    "roster": ("roster", "Team roster for a season", columns.ROSTER_COLUMN_NAMES),
    "play-by-play": (
        "play_by_play",
        "Game events identified by date and home team",
        columns.PLAY_BY_PLAY_COLUMN_NAMES,
    ),
    "contracts": ("contracts", "Current player contracts (JSON only)", None),
}

# Commands addressed by one or more season end years. Their CLI records are
# tagged with season_end_year because one invocation can combine seasons.
SEASON_ARGUMENT_COMMANDS = {
    "standings",
    "season-schedule",
    "players-season-totals",
    "players-advanced-season-totals",
    "players-regular-season-shooting-statistics",
    "roster",
    "regular-season-player-box-scores",
    "playoff-player-box-scores",
}
PLAYER_ARGUMENT_COMMANDS = {
    "regular-season-player-box-scores",
    "playoff-player-box-scores",
}
DATE_ARGUMENT_COMMANDS = {
    "player-box-scores",
    "team-box-scores",
    "play-by-play",
}
# Commands whose work contains independent fetches that --jobs may parallelize.
CONCURRENCY_COMMANDS = SEASON_ARGUMENT_COMMANDS | {"team-box-scores"}
MAX_JOBS = 16


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        _error("invalid_arguments", message)
        self.exit(2)


class JSONEncoder(BasketballReferenceJSONEncoder):
    def default(self, obj):
        if is_dataclass(obj) and not isinstance(obj, type):
            return asdict(obj)
        if isinstance(obj, Decimal):
            # Salaries retain exact decimal values rather than rounding to floats.
            return str(obj)
        return super().default(obj)


def _error(kind, message, **details):
    print(
        json.dumps({"error": {"type": kind, "message": message, **details}}),
        file=sys.stderr,
    )


def _season(value):
    try:
        year = int(value)
        if not 1 <= year <= 9999:
            raise ValueError
        return year
    except ValueError:
        raise argparse.ArgumentTypeError(
            "season must be an end year from 1 to 9999 (2018-19 is 2019)"
        )


def _date(value):
    try:
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
            raise ValueError
        return date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "date must be a valid YYYY-MM-DD calendar date"
        )


def _player(value):
    if not re.fullmatch(r"[a-z0-9]+", value):
        raise argparse.ArgumentTypeError(
            "player must be a lowercase identifier from search, such as jamesle01"
        )
    return value


def _term(value):
    if not value.strip():
        raise argparse.ArgumentTypeError("search term must not be blank")
    return value.strip()


def _team(value):
    normalized = " ".join(value.upper().split())
    for team in Team:
        if normalized == team.value or normalized.replace(" ", "_") == team.name:
            return team
    raise argparse.ArgumentTypeError(
        "unknown team; run 'basketball-reference teams' for accepted names"
    )


def _jobs(value):
    try:
        jobs = int(value)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError(
            f"jobs must be an integer from 1 to {MAX_JOBS}"
        )
    if not 1 <= jobs <= MAX_JOBS:
        raise argparse.ArgumentTypeError(
            f"jobs must be an integer from 1 to {MAX_JOBS}"
        )
    return jobs


def build_parser():
    parser = ArgumentParser(
        prog="basketball-reference",
        description="Scrape Basketball Reference. Results are JSON by default; errors are JSON on stderr.",
        epilog="Run COMMAND --help for arguments. Seasons use the ending year: 2018-19 = 2019.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    teams = commands.add_parser(
        "teams", help="List accepted team names without a network request"
    )
    teams.add_argument("--format", choices=["json"], default="json")
    teams.add_argument(
        "--output",
        type=Path,
        help="Write to this file instead of stdout; parent directory must exist",
    )
    teams.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing output file atomically",
    )
    for name, (function, description, schema) in OPERATIONS.items():
        command = commands.add_parser(name, help=description, description=description)
        command.add_argument(
            "--format", choices=["json", "csv"] if schema else ["json"], default="json"
        )
        command.add_argument(
            "--output",
            type=Path,
            help="Write to this file instead of stdout; parent directory must exist",
        )
        command.add_argument(
            "--overwrite",
            action="store_true",
            help="Replace an existing output file atomically",
        )
        if schema and name in SEASON_ARGUMENT_COMMANDS:
            # One CLI invocation may merge seasons, so CLI rows state their season.
            schema = ["season_end_year", *schema]
        if name in CONCURRENCY_COMMANDS:
            command.add_argument(
                "--jobs",
                type=_jobs,
                default=1,
                help=(
                    "Concurrent independent fetches, 1-"
                    f"{MAX_JOBS} (default 1; stop on 403 or 429)"
                ),
            )
        if name == "search":
            command.add_argument(
                "term", type=_term, help="Player name; quote names containing spaces"
            )
        if name in SEASON_ARGUMENT_COMMANDS:
            command.add_argument(
                "--season",
                type=_season,
                action="append",
                required=True,
                help="Season END year (2018-19 = 2019); repeat to combine seasons",
            )
        if name in DATE_ARGUMENT_COMMANDS:
            command.add_argument(
                "--date", type=_date, required=True, help="Calendar date YYYY-MM-DD"
            )
        if name in PLAYER_ARGUMENT_COMMANDS:
            command.add_argument(
                "--player",
                type=_player,
                action="append",
                required=True,
                help="Identifier returned by search; repeat to combine players",
            )
            command.add_argument("--include-inactive-games", action="store_true")
        if name == "players-advanced-season-totals":
            command.add_argument(
                "--include-combined-values",
                action="store_true",
                help="Include combined multi-team rows; avoid double-counting them",
            )
        if name in {"roster", "play-by-play"}:
            command.add_argument(
                "--team" if name == "roster" else "--home-team",
                type=_team,
                required=True,
                help="Team enum name or quoted full name; see teams",
            )
        command.set_defaults(function=function, schema=schema)
    return parser


def _run(tasks, function, jobs):
    if jobs > 1 and len(tasks) > 1:
        with ThreadPoolExecutor(max_workers=jobs) as executor:
            return list(executor.map(function, tasks))
    return [function(task) for task in tasks]


def _fetch(args):
    if args.command == "contracts":
        result = []
        client.contracts(contract_processor=result.append)
        return result
    if args.command == "search":
        return client.search(term=args.term)
    if args.command in DATE_ARGUMENT_COMMANDS:
        kwargs = dict(year=args.date.year, month=args.date.month, day=args.date.day)
        if args.command == "team-box-scores":
            kwargs["max_workers"] = args.jobs
        if args.command == "play-by-play":
            kwargs["home_team"] = args.home_team
        return getattr(client, args.function)(**kwargs)

    players = getattr(args, "player", None) or [None]
    # players-major, then the requested season order, so concatenated output is
    # deterministic and preserves the order the caller typed.
    tasks = [(player, season) for player in players for season in args.season]
    single_season = len(args.season) == 1

    def fetch(task):
        player, season = task
        kwargs = {"season_end_year": season}
        if player is not None:
            kwargs["player_identifier"] = player
        if hasattr(args, "include_inactive_games"):
            kwargs["include_inactive_games"] = args.include_inactive_games
        if hasattr(args, "include_combined_values"):
            kwargs["include_combined_values"] = args.include_combined_values
        if hasattr(args, "team"):
            kwargs["team"] = args.team
        # Parallelize inside the operation for a single season; with several
        # seasons the outer pool already keeps every worker busy.
        if args.command == "season-schedule" and single_season:
            kwargs["max_workers"] = args.jobs
        return getattr(client, args.function)(**kwargs)

    records = []
    for (_, season), rows in zip(tasks, _run(tasks, fetch, args.jobs)):
        for row in rows:
            row["season_end_year"] = season
            records.append(row)
    return records


def _serialize(data, args):
    if args.format == "json":
        return (
            json.dumps(
                data, cls=JSONEncoder, ensure_ascii=False, indent=2, allow_nan=False
            )
            + "\n"
        )
    rows = data["players"] if args.command == "search" else data
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=args.schema)
    writer.writeheader()
    writer.writerows(
        {key: format_value(value) for key, value in row.items()} for row in rows
    )
    return buffer.getvalue()


def _write_file(path, text, overwrite):
    # Render before opening anything; publish only the complete result. link()
    # implements create-if-absent without a check-then-overwrite race.
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=path.parent, delete=False
        ) as output:
            temporary = Path(output.name)
            output.write(text)
        # NamedTemporaryFile is created 0600; publish with the umask default so
        # exports stay readable by other users and overwrite does not tighten modes.
        umask = os.umask(0)
        os.umask(umask)
        os.chmod(temporary, 0o666 & ~umask)
        if overwrite:
            os.replace(temporary, path)
        else:
            os.link(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "overwrite", False) and args.output is None:
        parser.error("--overwrite requires --output")
    try:
        path = getattr(args, "output", None)
        if path is not None:
            if not path.parent.is_dir():
                raise FileNotFoundError(
                    f"Output directory does not exist: {path.parent}"
                )
            if path.exists() and not args.overwrite:
                raise FileExistsError(
                    f"Output already exists: {path}; use --overwrite to replace it"
                )
        data = [team.name for team in Team] if args.command == "teams" else _fetch(args)
        text = _serialize(data, args)
        if path is None:
            sys.stdout.write(text)
        else:
            _write_file(path, text, args.overwrite)
        return 0
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else None
        message = str(exc)
        if status == 403:
            message = "Basketball Reference denied this request (403). Stop and report the access failure."
        elif status == 429:
            message = "Basketball Reference rate limited this request (429). Stop and retry later."
        _error("http_error", message, status_code=status)
    except requests.exceptions.RequestException as exc:
        _error("network_error", str(exc))
    except (
        InvalidDate,
        InvalidPlayerAndSeason,
        InvalidSeason,
        InvalidTeamSeason,
    ) as exc:
        _error("invalid_resource", str(exc))
    except CouldNotGetPlayerContractData as exc:
        _error("http_error", str(exc))
    except OSError as exc:
        _error("output_error", str(exc))
    except Exception as exc:
        _error("scrape_error", f"{type(exc).__name__}: {exc}")
    return 1
