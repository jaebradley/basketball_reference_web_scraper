# Basketball Reference Web Scraper

[![Build Status](https://travis-ci.org/jaebradley/basketball_reference_web_scraper.svg?branch=master)](https://travis-ci.org/jaebradley/basketball_reference_web_scraper)
[![PyPI version](https://badge.fury.io/py/basketball_reference_web_scraper.svg)](https://badge.fury.io/py/basketball_reference_web_scraper)
[![codecov](https://codecov.io/gh/jaebradley/basketball_reference_web_scraper/branch/master/graph/badge.svg)](https://codecov.io/gh/jaebradley/basketball_reference_web_scraper)

[Basketball Reference](http://www.basketball-reference.com) is a great site (especially for a basketball stats nut like me), and hopefully they don't get too pissed off at me for creating this.

Basically, I created this repository as a utility for another project where I'm trying to estimate an NBA player's productivity as it relates to daily fantasy sports.  For that project, I need box score and scheduling information, which is provided by this utility. 

Here's the [PyPi package](https://pypi.python.org/pypi/basketball_reference_web_scraper/3.0).

## Installing via pip

I wrote this library as an exercise for creating my first `PyPi` package.  

Hopefully this means that if you'd like to use this library, you can by simply downloading the package via [pip](https://pypi.python.org/pypi/pip) like so

```bash
pip install basketball_reference_web_scraper
```

This library requires `Python 3.4+` and only supports seasons after the `1999-2000` season

## Client

You can import the `client` like this

```python
# This imports the client
from basketball_reference_web_scraper import client
```

There are also a couple useful `enum`s that are defined in the `data` module which can be `import`ed like

```python
# This imports the Team enum
from basketball_reference_web_scraper.data import Team
```

## API

This client has four methods
* Getting player box scores by a date (`client.player_box_scores`)
* Getting team box scores by a date (`client.team_box_scores`)
* Getting the schedule for a season (`client.season_schedule`)
* Getting players totals for a season (`client.players_season_totals`)

You can see all four methods used in [this `repl`]()https://repl.it/@jaebradley/v300api-examples).

### Data output

This client also supports three output types:
* Python data types (i.e. a `list` or results)
* `JSON`
* `CSV`

Versions `>=3` of this client outputs `CSV` to a specified file path and returns `JSON` output or writes it to a specified file path.
* Specify an output type by setting the `output_type` value to `OutputType.JSON` or `OutputType.CSV`
  * The default return value of client methods are `Python` data structures (the `box_scores` method returns a `list` of `dict`s)
* If you'd like the output to be outputted to a specific file, set the `output_file_path` variable - for `CSV` output, this variable must be defined
* Specifying an `output_write_option` specifies how the output will be written to the specified file (`OutputWriteOption.WRITE` corresponds to `w`)
  * The default write option is `OutputWriteOption.WRITE`

### Data parsing

* Some pieces of data, like a player's team or the outcome of a game are parsed into enums (for example, the `Team` and `Outcome` enums, respectively, for the previous two examples)
* These enums are serialized to strings when outputting to `JSON` or `CSV`, but when dealing with `Python` data structures, you'll see these enum values.
  * Hopefully, these enums make it easier for the `client `user to implement team-specific logic, for example.  


### Get player box scores by date

```python
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType

# Get all player box scores for January 1st, 2017 
client.player_box_scores(day=1, month=1, year=2017)

# Get all player box scores for January 1st, 2017 in JSON format
client.player_box_scores(day=1, month=1, year=2017, output_type=OutputType.JSON)

# Output all player box scores for January 1st, 2017 in JSON format to 1_1_2017_box_scores.json
client.player_box_scores(day=1, month=1, year=2017, output_type=OutputType.JSON, output_file_path="./1_1_2017_box_scores.json")

# Output all player box scores for January 1st, 2017 in JSON format to 1_1_2017_box_scores.csv
client.player_box_scores(day=1, month=1, year=2017, output_type=OutputType.CSV, output_file_path="./1_1_2017_box_scores.csv")
```

### Get team box scores by date

```python
from basketball_reference_web_scraper import client

# Get all team totals for January 1st, 2018
client.team_box_scores(day=1, month=1, year=2018)

# The team_box_scores method also supports all output behavior previously described
```

### Get season schedule

```python
from basketball_reference_web_scraper import client

# Get all games for the 2017-2018 season
client.season_schedule(season_end_year=2018)

# The schedule method also supports all output behavior previously described
``` 

### Get season totals for all players

 ```python
from basketball_reference_web_scraper import client

# Get 2017-2018 season totals for all players
client.players_season_totals(season_end_year=2018)

# The players_season_totals method also supports all output behavior previously described
```

## Development

There are currently two supported major versions - `V3` and `V4`.

There are two branches, `v3` and `v4` for both of these major versions - these are the defacto "master" branches to use
when making changes.

`master` will reflect the latest major version branch.

