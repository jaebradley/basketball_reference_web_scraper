# Development

## Branches

There are two branches, `v3` and `v4`, which map to the `3+` and `4+` versions, respectively. These are the defacto 
branches to branch from when developing features.

The `v3` branch (as well as the `3+` version) will be deprecated in the near-future.

`master` will reflect the latest major version branch.

## Local

Install dependencies using [`poetry`](https://python-poetry.org/) - for installation directions, see 
[the documentation](https://python-poetry.org/docs/).

Once `poetry` has been installed, dependencies can be installed using the `install` command like

```bash
poetry install
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
    Sometimes the suite of integration tests run into rate-limiting errors - I'm currently thinking of ways to mitigate
    this behavior.

Currently, this project uses [**Codecov**](https://codecov.io/gh/jaebradley/basketball_reference_web_scraper) for code 
coverage statistics.

## Continuous Integration

[**GitHub Actions**](https://github.com/jaebradley/basketball_reference_web_scraper/actions) is used for continuous 
integration to run tests on a variety of operating systems.

