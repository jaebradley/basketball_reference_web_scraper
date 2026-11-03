# Using Basketball Reference Web Scraper

For requests such as “use basketball reference web scraper to …”, follow
[the task skill](.agents/skills/basketball-reference-web-scraper/SKILL.md).
It covers selecting the data, resolving players, executing the CLI, and verifying
the requested result. CLI setup and examples are in [docs/agents.md](docs/agents.md).

For code changes, run the offline suite with
`uv run pytest --ignore="tests/end to end/"`. The end-to-end directory makes live
requests; the integration directory uses recorded HTML and mocked HTTP.
