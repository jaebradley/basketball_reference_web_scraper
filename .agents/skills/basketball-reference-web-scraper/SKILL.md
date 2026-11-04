---
name: basketball-reference-web-scraper
description: Use Basketball Reference Web Scraper to retrieve NBA schedules, standings, rosters, player or team box scores, game logs, play-by-play, season statistics, shooting statistics, or current contracts, and analyze or export the results.
---

# Basketball Reference tasks

Use the `basketball-reference` CLI with shell access and Python 3.10+. In a source
checkout, run `uv sync`, then prefix commands with `uv run`. Alternatively install
the checkout with `python -m pip install .` and use
`python -m basketball_reference_web_scraper`. Run `--help` and the selected
command's `--help` to discover arguments. If the installed version has no CLI,
install a checkout containing this skill. A chat-only agent needs a shell-enabled
runner; this package does not itself supply an MCP server.

1. Translate the request into data grain, date or season, regular season or
   playoffs, requested metrics, and destination. `--season` is the **ending**
   year: 2018-19 is 2019. Resolve material ambiguity with the user. Use separate
   regular-season and playoff game-log commands; season totals and advanced
   totals are regular season. Historical NBA coverage varies; WNBA and college
   data are outside this package's supported scope.
2. Resolve player names with `search "Name"`. Read its `players` list and use the
   matching `identifier` for `--player`; disambiguate multiple matches before
   fetching. For a team use the enum name from `teams`. `play-by-play` requires
   the **home** team and the calendar date; find these in `season-schedule` when
   the request supplies only an opponent or an away team.
3. Fetch only the required data. JSON is the default; supported flat tables also
   accept `--format csv`. Combine work in one invocation by repeating `--player`
   and `--season`; rows are emitted in request order and tagged with the
   requested `season_end_year`. Add `--jobs N` (1-16) to fetch independent pages
   or player-seasons concurrently; the default is sequential. Use `--output
   PATH` to save; add `--overwrite` only when replacing that file is intended.
   Set a finite runner deadline appropriate to the task (for example, 120
   seconds for one lookup; schedules can make several requests). On deadline
   expiry stop the process and report incomplete work. The CLI performs no
   automatic retries.
4. Check the exit status before parsing stdout or reading an export. Failures
   produce a JSON `error` on stderr: exit 2 means invalid arguments; exit 1 means
   fetch, parse, or output failure. On 403 or 429, stop and report the access or
   rate limit failure. Preserve partial task progress when doing multiple calls;
   report which calls succeeded. An empty result establishes no matching rows,
   not a zero-valued statistic or proof of complete source coverage.
5. Compute the requested answer from the returned rows. Game-log rows carry
   `player_identifier`; schedule rows carry the source game `date` as well as the
   UTC `start_time`, so join on `date`. Avoid double-counting combined and
   team-specific rows for traded players (advanced totals offer
   `--include-combined-values`). Check the actual output fields before computing
   a metric; a box score may require deriving points from made shots, and minute
   totals may be represented as seconds. Contracts use **season start years**
   and exact decimal salary strings, unlike the `--season` argument.
6. Verify the saved file parses, its row count and requested scope, and any
   calculation. Deliver the requested answer or artifact, with dates/season,
   phase, source commands, and relevant coverage limitations. Completion means
   the user's analysis/export exists and has been checked, not just that a
   command or script has been proposed.
