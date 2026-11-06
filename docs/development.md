# Development

## Branches

There is one main development branch (`v4`) that maps to the current major version (`4.x.x`). Any future major version 
development branches will reflect this pattern (i.e. the `v5` branch contains changes associated with the next major version `5.x.x`).

## Local

Install dependencies using [`uv`](https://docs.astral.sh/uv) - for installation directions, see 
[the documentation](https://docs.astral.sh/uv/).

Once `uv` has been installed, dependencies can be installed using the `sync` command like

```bash
uv sync
```

!!! note
    The `pyproject.toml` file is used to describe the project's requirements and relevant metadata including both the
    project's dependencies and it's development dependencies (like for generating code coverage, and this documentation 
    site)

## Testing

Unit tests are organized in the `unit` directory under the `tests` directory while integration tests are organized 
under the `integration` directory.

In the cases where tests are extensive (like integration tests for an API method), each of these tests are grouped in a 
separate file, even if they are implemented in the same file.

This is why API methods have their own integration test file under the `client` directory even though they are all 
implemented in the `client.py` file.

!!! warning
    The `end to end` tests execute live HTTP requests to basketball-reference.com and sometimes run into rate-limiting errors. The `unit` and `integration` suites run offline - the `integration` directory uses recorded HTML and mocked HTTP.

Run the offline suite with

```bash
uv run pytest --ignore="tests/end to end/"
```

Currently, this project uses [**Codecov**](https://codecov.io/gh/jaebradley/basketball_reference_web_scraper) for code coverage statistics.

## Continuous Integration

[**GitHub Actions**](https://github.com/jaebradley/basketball_reference_web_scraper/actions) is used for continuous integration to run tests on a variety of operating systems.

