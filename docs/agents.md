# Use with agents and the command line

An agent with shell access can use this package to fetch NBA data and complete
analysis or export tasks. Give it this repository and a request such as:

> Use basketball reference web scraper to export Russell Westbrook's 2018-19
> regular-season game log to westbrook-2019.csv, then report his average points
> across active games.

Repository agents can find the workflow through `AGENTS.md` and the bundled
`.agents/skills/basketball-reference-web-scraper/SKILL.md`. For another skill-aware
runner, copy that skill directory into its skills directory. For other shell
agents, provide the skill file as task instructions. Installing the Python
package provides the CLI; it does not configure a runner or register an MCP
server. A chat-only agent needs a shell tool supplied by its host.

## Install this checkout

The CLI must be installed from a version containing `cli.py`. These commands use
the checked-out source, so they also work before a new PyPI release:

```bash
python -m pip install .
basketball-reference --help
```

Python 3.10+ is required. The equivalent module entry point is:

```bash
python -m basketball_reference_web_scraper --help
```

For development, `uv sync` installs this checkout and its dependencies; use
`uv run basketball-reference ...`. Help and `teams` work offline. All other
commands fetch Basketball Reference and depend on its availability and HTML.

## Lookup, fetch, verify

```bash
basketball-reference search "Russell Westbrook"
```

Read `players[].identifier` from the JSON response. Select the correct player;
use that identifier, rather than inferring it from their name:

```bash
basketball-reference regular-season-player-box-scores --player westbru01 --season 2019 --format csv --output westbrook-2019.csv
```

`--season 2019` means 2018-19. Playoffs use
`playoff-player-box-scores` separately. To finish the example analysis, read the
saved CSV, select active rows, compute the average of `points_scored`, and report
the row count and result. Include `--include-inactive-games` when inactive rows
are part of the requested export. Inspect the response fields before analysis;
different endpoints have different schemas and units.

Repeat `--player` and `--season` to combine several game logs in one invocation.
Rows are emitted in request order (player-major). Game-log rows carry
`player_identifier`, and every season-scoped CLI row carries its
`season_end_year`, so merged exports stay attributable:

```bash
basketball-reference regular-season-player-box-scores \
  --player westbru01 --player hardeja01 \
  --season 2018 --season 2019 \
  --jobs 4 --format csv --output game-logs.csv
```

`--jobs` runs independent page fetches concurrently for schedule months and team
box scores; it applies to `--season` and game-log commands too, where each
player-season is independent. It defaults to 1 (sequential). Sequential client
calls in one thread reuse a shared connection pool, so a multi-player batch does
not repeat DNS/TLS setup per player. Requests still stop on 403 or 429. Rows from
repeated seasons combine, and the CLI replaces any source-provided
`season_end_year` with the requested season so tags are exact. The Python API
stays per-season and does not add `season_end_year`.

Other examples:

```bash
basketball-reference teams
basketball-reference roster --team BOSTON_CELTICS --season 2019
basketball-reference player-box-scores --date 2018-01-01
basketball-reference season-schedule --season 2018 --season 2019 --jobs 4 --output schedule.json
basketball-reference play-by-play --home-team TORONTO_RAPTORS --date 2003-10-29
basketball-reference players-advanced-season-totals --season 2019 --include-combined-values
```

Full quoted team names such as `"Boston Celtics"` also work. Abbreviations such
as `BOS` are not accepted; `teams` lists accepted enum names. For play-by-play,
use the home team, which may differ from the team named in the request.

## Choose a command

Run `basketball-reference COMMAND --help` for required arguments and supported
formats. Each command corresponds to the Python API function with underscores
in place of hyphens (except `--season`, `--player`, and `--date`, which expand to
the API's season end year, player identifier, and day/month/year arguments).

| Request | Command |
| --- | --- |
| Player name → identifier | `search` |
| Division standings | `standings` |
| All players or teams on one day | `player-box-scores`, `team-box-scores` |
| One player's game log | `regular-season-player-box-scores`, `playoff-player-box-scores` |
| Season schedule | `season-schedule` |
| Regular-season player totals | `players-season-totals` |
| Advanced regular-season totals | `players-advanced-season-totals` |
| Nested shooting statistics | `players-regular-season-shooting-statistics` |
| Team roster | `roster` |
| Game events | `play-by-play` |
| Current contracts | `contracts` |

The CLI can combine repeated `--season` and `--player` values in one request.
Filtering, ranking, aggregation, charts, and cross-command joins are performed by
the agent using the retrieved rows. Combined multi-team rows and individual-team
rows must not both be summed for the same player. The package targets NBA data;
historical coverage varies and ABA/BAA support is incomplete. Contracts are
current data, not a historical-season query.

## Output and failures

- Successful calls exit 0. JSON goes to stdout by default; `search` returns an
  object with a `players` array, `teams` returns enum names, and other commands
  return arrays of records. Dates are ISO strings, enums are their values, and
  sets become arrays. Contract salary amounts are exact decimal strings and
  salary-map keys are season **start** years. Shooting and contracts support
  JSON only because they contain nested data. Every season-scoped CLI record
  includes `season_end_year`, so repeated-season output stays attributable.
  Game-log records include `player_identifier`. Schedule records expose the
  source game `date` alongside the UTC `start_time`; join on `date`, not on the
  UTC calendar date of `start_time`.
- Flat endpoints accept `--format csv`, including a header for empty results.
  Search CSV contains the player rows. Without `--output`, CSV goes to stdout.
- `--output PATH` writes UTF-8 to an existing directory, with empty stdout. A
  file is published only after fetching and serialization succeed. An existing
  path is preserved unless `--overwrite` is supplied; replacement is atomic.
  No success message is mixed into result data.
- Argument errors exit 2. Runtime errors exit 1. Both emit a JSON object of the
  form `{"error": {"type": "...", "message": "..."}}` on stderr. HTTP errors
  include `status_code` when available. Empty data is a successful fetch, but
  does not prove source completeness. Check exit status before using output.
- The CLI does not retry failures. Stop on access denial (403) or rate limiting
  (429), report the failure, and retry later if appropriate. Requests are
  sequential by default; `--jobs N` opts into bounded concurrency for independent
  pages and player-seasons and still stops on access denial or rate limiting.
  Use a finite deadline in the agent runner, especially for schedules and other
  commands making multiple requests. Report failed or incomplete requests
  instead of inventing missing results.

The existing [Python API](api.md) remains available for direct integrations.
