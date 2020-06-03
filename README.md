# Basketball Reference Web Scraper

![PyPI](https://img.shields.io/pypi/v/basketball_reference_web_scraper)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/basketball_reference_web_scraper)
![PyPI - License](https://img.shields.io/pypi/l/basketball_reference_web_scraper)
[![codecov](https://codecov.io/gh/jaebradley/basketball_reference_web_scraper/branch/v4/graph/badge.svg)](https://codecov.io/gh/jaebradley/basketball_reference_web_scraper)
![GitHub Actions - Default Branch](https://github.com/jaebradley/basketball_reference_web_scraper/workflows/Basketball%20Reference%20Web%20Scraper/badge.svg)

[Basketball Reference](http://www.basketball-reference.com) is a great site (especially for a basketball stats nut like me), and hopefully they don't get too pissed off at me for creating this.

Basically, I created this repository as a utility for another project where I'm trying to estimate an NBA player's productivity as it relates to daily fantasy sports.  For that project, I need box score and scheduling information, which is provided by this utility. 

Here's the [PyPi package](https://pypi.org/project/basketball-reference-web-scraper/).

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

This client has seven methods
* Getting player box scores by a date (`client.player_box_scores`)
* Getting team box scores by a date (`client.team_box_scores`)
* Getting the schedule for a season (`client.season_schedule`)
* Getting players totals for a season (`client.players_season_totals`)
* Getting players advanced season statistics for a season (`client.players_advanced_season_totals`)
* Getting regular season box scores for a given player and season (`client.regular_season_player_box_scores`)
* Searching (`client.search`)

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

* [`repl.it` Examples](https://repl.it/@jaebradley/PlayerBoxScoresByDate#main.py)

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

* [`repl.it` Examples](https://repl.it/@jaebradley/TeamBoxScoresByDate#main.py)

```python
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType

# Get all team box scores for January 1st, 2018 
client.team_box_scores(day=1, month=1, year=2018)

# Get all team box scores for January 1st, 2018 in JSON format
client.team_box_scores(day=1, month=1, year=2018, output_type=OutputType.JSON)

# Output all team box scores for January 1st, 2018 in JSON format to 1_1_2018_box_scores.json
client.team_box_scores(day=1, month=1, year=2018, output_type=OutputType.JSON, output_file_path="./1_1_2018_box_scores.json")

# Output all team box scores for January 1st, 2018 in JSON format to 1_1_2018_box_scores.csv
client.team_box_scores(day=1, month=1, year=2018, output_type=OutputType.CSV, output_file_path="./1_1_2018_box_scores.csv")
```

### Get season schedule

* [`repl.it` Examples](https://repl.it/@jaebradley/SeasonSchedule#main.py)

```python
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType

# Get all games for the 2017-2018 season
client.season_schedule(season_end_year=2018)

# Get all games for the 2017-2018 season and output in JSON format
client.season_schedule(season_end_year=2018, output_type=OutputType.JSON)

# Output all games for the 2017-2018 season in CSV format to 2017_2018_season.csv
client.season_schedule(season_end_year=2018, output_type=OutputType.JSON, output_file_path="./2017_2018_season.json")

# Output all games for the 2017-2018 season in CSV format to 2017_2018_season.csv
client.season_schedule(season_end_year=2018, output_type=OutputType.CSV, output_file_path="./2017_2018_season.csv")
``` 

### Get season totals for all players

* [`repl.it` Examples](https://repl.it/@jaebradley/PlayerSeasonTotals#main.py)

```python
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType

# Get all player season totals for the 2017-2018 season
client.players_season_totals(season_end_year=2018)

# Get all player season totals for the 2017-2018 season and output in JSON format
client.players_season_totals(season_end_year=2018, output_type=OutputType.JSON)

# Output all player season totals for the 2017-2018 season in JSON format to 2017_2018_player_season_totals.json
client.players_season_totals(season_end_year=2018, output_type=OutputType.JSON, output_file_path="./2017_2018_player_season_totals.json")

# Output all player season totals for the 2017-2018 season in CSV format to 2017_2018_player_season_totals.csv
client.players_season_totals(season_end_year=2018, output_type=OutputType.CSV, output_file_path="./2017_2018_player_season_totals.csv")
```

### Get advanced season statistics for all players

* [`repl.it` Examples](https://repl.it/@jaebradley/PlayerAdvancedSeasonTotals#main.py)

```python
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType

# Get all advanced player season totals for the 2017-2018 season
client.players_advanced_season_totals(season_end_year=2018)

# Get all advanced player season totals for the 2017-2018 season and output in JSON format
client.players_advanced_season_totals(season_end_year=2018, output_type=OutputType.JSON)

# Output all advanced player season totals for the 2017-2018 season in JSON format to 2017_2018_player_season_totals.json
client.players_advanced_season_totals(season_end_year=2018, output_type=OutputType.JSON, output_file_path="./2017_2018_advanced_player_season_totals.json")

# Output all advanced player season totals for the 2017-2018 season in CSV format to 2017_2018_player_season_totals.csv
client.players_advanced_season_totals(season_end_year=2018, output_type=OutputType.CSV, output_file_path="./2017_2018_advanced_player_season_totals.csv")
```

### Get play-by-play data for a game

* [`repl.it` Examples](https://repl.it/@jaebradley/PlayByPlay#main.py)

The structure of the API is due to the unique URL pattern that Basketball Reference has for getting play-by-play data, 
which depends on the date of the game and the home team.

Example: `https://www.basketball-reference.com/boxscores/pbp/201810160BOS.html`

```python
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType, Team

# Get play-by-play for Boston Celtics game on October 16th, 2018
client.play_by_play(home_team=Team.BOSTON_CELTICS, year=2018, month=10, day=16)

# Get play-by-play for Boston Celtics game on October 16th, 2018 and output in JSON format
client.play_by_play(home_team=Team.BOSTON_CELTICS, year=2018, month=10, day=16, output_type=OutputType.JSON)

# Get play-by-play for Boston Celtics game on October 16th, 2018  in JSON format to 2018_10_06_BOS_PBP.json
client.play_by_play(home_team=Team.BOSTON_CELTICS, year=2018, month=10, day=16, output_type=OutputType.JSON, output_file_path="./2018_10_06_BOS_PBP.json")

# Output all advanced player season totals for the 2017-2018 season in CSV format to 2018_10_06_BOS_PBP.csv
client.play_by_play(home_team=Team.BOSTON_CELTICS, year=2018, month=10, day=16, output_type=OutputType.CSV, output_file_path="./2018_10_06_BOS_PBP.csv")
```

### Get regular season box scores for a player

* [`repl.it` Examples](https://repl.it/@jaebradley/RegularSeasonPlayerBoxScores#main.py)

```python
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType

# Get all 2017-2018 regular season player box scores for Russell Westbrook
client.regular_season_player_box_scores(player_identifier="westbru01", season_end_year=2018)

# Get all 2017-2018 regular season player box scores for Russell Westbrook in JSON format
client.regular_season_player_box_scores(player_identifier="westbru01", season_end_year=2018, output_type=OutputType.JSON)

# Output all 2017-2018 regular season player box scores for Russell Westbrook in JSON format to 2017_2018_russell_westbrook_regular_season_box_scores.json
client.regular_season_player_box_scores(player_identifier="westbru01", season_end_year=2018, output_type=OutputType.JSON, output_file_path="./2017_2018_russell_westbrook_regular_season_box_scores.json")

# Output all 2017-2018 regular season player box scores for Russell Westbrook in CSV format to 2017_2018_russell_westbrook_regular_season_box_scores.csv
client.regular_season_player_box_scores(player_identifier="westbru01", season_end_year=2018, output_type=OutputType.CSV, output_file_path="./2017_2018_russell_westbrook_regular_season_box_scores.csv")
```

The `player_identifier` is Basketball Reference's unique identifier for each player. In the case of Russell Westbrook,
his `player_identifier` is `westbru01` (you can see this from his player page URL: 
`https://www.basketball-reference.com/players/w/westbru01/gamelog/2020`)

### Search 

* [`repli.t` Examples](https://repl.it/@jaebradley/Search#main.py)

```python
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType

# Get all results that match "Ko"
client.search(term="Ko")

# Get all results that match "Ko" and output in JSON format
client.search(term="Ko", output_type=OutputType.JSON)

# Output all results that match "Ko" in JSON format to ko_search.json
client.search(term="Ko", output_type=OutputType.JSON, output_file_path="./ko_search.json")

# Output all results that match "Ko" in CSV format to ko_search.csv
client.search(term="Ko", output_type=OutputType.CSV, output_file_path="./ko_search.csv")
```

## Development

There are currently two supported major versions - `V3` and `V4`.

There are two branches, `v3` and `v4` for both of these major versions - these are the defacto "master" branches to use
when making changes.

`master` will reflect the latest major version branch.

## Contributors

Thanks to [@DaiJunyan](https://github.com/DaiJunyan), [@ecallahan5](https://github.com/ecallahan5), 
[@Yotamho](https://github.com/Yotamho), and [@ntsirakis](https://github.com/ntsirakis) for their contributions!

