<p align="center">
    <a href="#" target="_blank" rel="noopener noreferrer">
        <img width="550" src="https://imgur.com/dJL05Ud.png" alt="logo">
    </a>
</p>
<p align="center">
    <a href="https://pypi.org/project/basketball_reference_web_scraper/">
        <img src="https://img.shields.io/pypi/v/basketball_reference_web_scraper" alt="pypi" />
    </a>
    <a href="https://pypi.org/project/basketball_reference_web_scraper/">
        <img src="https://img.shields.io/pypi/pyversions/basketball_reference_web_scraper" alt="python version" />
    </a>
    <a href="https://pypi.org/project/basketball_reference_web_scraper/">
        <img src="https://img.shields.io/pypi/l/basketball_reference_web_scraper" alt="license" />
    </a>
    <a href="https://codecov.io/gh/jaebradley/basketball_reference_web_scraper">
        <img src="https://codecov.io/gh/jaebradley/basketball_reference_web_scraper/branch/v4/graph/badge.svg" alt="code coverage" />
    </a>
    <a href="https://github.com/jaebradley/basketball_reference_web_scraper/workflows/Build/badge.svg">
        <img src="https://github.com/jaebradley/basketball_reference_web_scraper/workflows/Build/badge.svg" alt="continuous integration" />
    </a>
</p>

[Basketball Reference](http://www.basketball-reference.com) is a great site (especially for a basketball stats nut like me), and hopefully they don't get too pissed off at me for creating this.

I initially wrote this library as an exercise for creating my first `PyPi` package - hope you find it valuable!  

## Documentation

For documentation about installing the package and API methods see [the documentation page](https://jaebradley.github.io/basketball_reference_web_scraper/).

## Use with agents

Ask a shell-enabled agent: “Use basketball reference web scraper to export
Russell Westbrook's 2018-19 regular-season game log to CSV and calculate his
average points.” This repository includes an [agent task skill](.agents/skills/basketball-reference-web-scraper/SKILL.md)
and a JSON-first CLI covering all public client operations.

Install this checkout with `python -m pip install .`, then run
`basketball-reference --help` (or `python -m basketball_reference_web_scraper --help`).
See the [agent and CLI guide](docs/agents.md) for setup, examples, and output and
failure contracts.

## Contributors

Thanks to [@DaiJunyan](https://github.com/DaiJunyan), [@ecallahan5](https://github.com/ecallahan5), 
[@Yotamho](https://github.com/Yotamho), [@ntsirakis](https://github.com/ntsirakis), [@allanbelliti](https://github.com/allanbelliti), [@krlu](https://github.com/krlu), [@aaronbannin](https://github.com/aaronbannin), [@benjaminmesser](https://github.com/benjaminmesser), [@pepeefirat](https://github.com/pepeefirat), [@PGats](https://github.com/PGatts), [@jakeakopp](https://github.com/jakeakopp), and [@DigitalCurrensy](https://github.com/DigitalCurrensy) for their contributions!

