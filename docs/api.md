# API

## Client

The `import`ed `client` contains the API methods that will access **Basketball Reference**

```python
from basketball_reference_web_scraper import client
```

## Enums

Various `enum` values are returned as part of the result set for API methods **_or_** as inputs for various API methods.

They are `import`ed from the `data` path.

=== "League"
    ```python
    from basketball_reference_web_scraper.data import Location 
    ```
    
    !!! note
        Represents the league designated by **Basketball Reference**.
        
        The values are `League.NATIONAL_BASKETBALL_ASSOCIATION`, `League.AMERICAN_BASKETBALL_ASSOCIATION`, and 
        `League.BASKETBALL_ASSOCIATION_OF_AMERICA`.

=== "Location"
    ```python
    from basketball_reference_web_scraper.data import Location 
    ```
    
    !!! note
        Represents whether a game was played at home or away. 
        
        The two possible values are `Location.HOME` and `Location.AWAY`
        
=== "Outcome"
    ```python
    from basketball_reference_web_scraper.data import Outcome 
    ```
    
    !!! note
        Represents if a game ended in a win or a loss. 
        
        The two possible values are `Outcome.WIN` and `Outcome.LOSS`

=== "OutputType"
    ```python
    from basketball_reference_web_scraper.data import OutputType 
    ```
    
    !!! note
        Represents the type of data output.
        
        The two possible values are `OutputType.JSON` and `OutputType.CSV`

=== "OutputWriteOption"
    ```python
    from basketball_reference_web_scraper.data import OutputWriteOption 
    ```
    
    !!! note
        Represents Python file modes when outputting data.
        
        The four possible values are `OutputWriteOption.WRITE`, `OutputWriteOption.CREATE_AND_WRITE`, 
        `OutputWriteOption.APPEND`, and `OutputWriteOption.APPEND_AND_WRITE` 

=== "Position"
    ```python
    from basketball_reference_web_scraper.data import Position 
    ```
    
    !!! note
        Represents one of the seven positon designations (`Position.POINT_GUARD`, `Position.SHOOTING_GUARD`, `Position.SMALL_FORWARD`, 
        `Position.POWER_FORWARD`, `Position.CENTER`, `Position.FORWARD`, `Position.GUARD`) in **Basketball Reference**

=== "PeriodType"
    ```python
    from basketball_reference_web_scraper.data import PeriodType 
    ```
    
    !!! note
        Represents if a period was a quarter (`PeriodType.QUARTER`) or an overtime period (`PeriodType.OVERTIME`)
        
=== "Team"
    ```python
    from basketball_reference_web_scraper.data import Team
    ```
    
    !!! note
        Represents a team in the NBA (for example, `Team.BOSTON_CELTICS`).

## Output

The default data returned by API methods are Python objects (e.g. a `list` of `dictionaries`).

All API methods come with `output_type`, `output_file_path`, `output_write_option`, and `json_options` arguments that are
**_optional_**, and by default, are `None`.

These arguments can be used to specify `JSON` / `CSV` output that may be written to a file.

Use the `OutputType` `enum` as the `output_type` value to specify `CSV` or `JSON` output.

The `output_file_path` argument takes a string and specifies where the result output should be written.

!!! warning
    Currently, specifying an `output_type` of `OutputType.CSV` **requires** an `output_file_path` value.
    
    `JSON` output can be returned by API methods without having to be written to a file.

Use the `OutputWriteOption` `enum` as the `output_write_option` value to specify if the result output should be written,
or appended to the specified file path (or any of other the Python file mode options).

!!! note
    The default `OutputWriteOption` if it is **_not_** specified (but an `output_file_path` value **_is_** specified) is 
    `OutputWriteOption.WRITE`.

## Methods

### Player Box Scores For A Given Day

* [`repl.it` Examples](https://repl.it/@jaebradley/PlayerBoxScoresByDate#main.py)

=== "Python Data Structures"
    ```python
    from basketball_reference_web_scraper import client

    client.player_box_scores(day=1, month=1, year=2017)
    ```
    
=== "JSON"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.player_box_scores(day=1, month=1, year=2017, output_type=OutputType.JSON)
    ```

=== "JSON to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.player_box_scores(
        day=1, month=1, year=2017, 
        output_type=OutputType.JSON, 
        output_file_path="./1_1_2017_box_scores.json"
    )
    ```
       
=== "CSV to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.player_box_scores(
        day=1, month=1, year=2017, 
        output_type=OutputType.CSV, 
        output_file_path="./1_1_2017_box_scores.csv"
    )
    ```

### Team Box Scores For A Given Day

* [`repl.it` Examples](https://repl.it/@jaebradley/TeamBoxScoresByDate#main.py)

=== "Python Data Structures"
    ```python
    from basketball_reference_web_scraper import client

    client.team_box_scores(day=1, month=1, year=2018)
    ```
    
=== "JSON"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.team_box_scores(day=1, month=1, year=2017, output_type=OutputType.JSON)
    ```

=== "JSON to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.team_box_scores(
        day=1, month=1, year=2017, 
        output_type=OutputType.JSON, 
        output_file_path="./1_1_2017_box_scores.json"
    )
    ```
       
=== "CSV to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.team_box_scores(
        day=1, month=1, year=2017, 
        output_type=OutputType.CSV, 
        output_file_path="./1_1_2017_box_scores.csv"
    )
    ```
    
### Get Season Schedule

* [`repl.it` Examples](https://repl.it/@jaebradley/SeasonSchedule#main.py)

=== "Python Data Structures"
    ```python
    from basketball_reference_web_scraper import client

    client.season_schedule(season_end_year=2018)
    ```
    
=== "JSON"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.season_schedule(season_end_year=2018, output_type=OutputType.JSON)
    ```

=== "JSON to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType
    
    client.season_schedule(
        season_end_year=2018, 
        output_type=OutputType.JSON, 
        output_file_path="./2017_2018_season.json"
    )
    ```
       
=== "CSV to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.season_schedule(
        season_end_year=2018, 
        output_type=OutputType.CSV, 
        output_file_path="./2017_2018_season.csv"
    )
    ```

### Player Season Totals (Basic Statistics)

* [`repl.it` Examples](https://repl.it/@jaebradley/PlayerSeasonTotals#main.py)

=== "Python Data Structures"
    ```python
    from basketball_reference_web_scraper import client

    client.players_season_totals(season_end_year=2018)
    ```
    
=== "JSON"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.players_season_totals(season_end_year=2018, output_type=OutputType.JSON)
    ```

=== "JSON to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType
    
    client.players_season_totals(
        season_end_year=2018, 
        output_type=OutputType.JSON, 
        output_file_path="./2017_2018_player_season_totals.json"
    )
    ```
       
=== "CSV to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.players_season_totals(
        season_end_year=2018, 
        output_type=OutputType.CSV, 
        output_file_path="./2017_2018_player_season_totals.csv"
    )
    ```

### Player Season Totals (Advanced Statistics)

* [`repl.it` Examples](https://repl.it/@jaebradley/PlayerAdvancedSeasonTotals#main.py)

=== "Python Data Structures"
    ```python
    from basketball_reference_web_scraper import client

    client.players_advanced_season_totals(season_end_year=2018)
    ```
    
=== "JSON"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.players_advanced_season_totals(season_end_year=2018, output_type=OutputType.JSON)
    ```

=== "JSON to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType
    
    client.players_advanced_season_totals(
        season_end_year=2018, 
        output_type=OutputType.JSON, 
        output_file_path="./2017_2018_advanced_player_season_totals.json"
    )
    ```
       
=== "CSV to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType
    
    client.players_advanced_season_totals(
        season_end_year=2018,
        output_type=OutputType.CSV,
        output_file_path="./2017_2018_advanced_player_season_totals.csv"
    )
    ```

### Play-By-Play

* [`repl.it` Examples](https://repl.it/@jaebradley/PlayByPlay#main.py)

!!! note
    The structure of the API is due to the unique URL pattern that **Basketball Reference** has for getting play-by-play 
    data which depends on the date of the game and the home team.

=== "Python Data Structures"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import Team

    client.play_by_play(home_team=Team.BOSTON_CELTICS, year=2018, month=10, day=16)
    ```
    
=== "JSON"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType, Team

    client.play_by_play(
        home_team=Team.BOSTON_CELTICS, 
        year=2018, month=10, day=16, 
        output_type=OutputType.JSON
    )
    ```

=== "JSON to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType, Team
    
    client.play_by_play(
        home_team=Team.BOSTON_CELTICS, 
        year=2018, month=10, day=16, 
        output_type=OutputType.JSON, 
        output_file_path="./2018_10_06_BOS_PBP.json"
    )
    ```
       
=== "CSV to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType, Team

    client.play_by_play(
        home_team=Team.BOSTON_CELTICS, 
        year=2018, month=10, day=16, 
        output_type=OutputType.CSV, 
        output_file_path="./2018_10_06_BOS_PBP.csv"
    )
    ```

### Regular Season Player Box Scores

!!! note
    The `player_identifier` is **Basketball Reference's** unique identifier for each player. 
    
    In the case of Russell Westbrook, their `player_identifier` is **`westbru01`**.
    
    You can see this from their player page URL: https://www.basketball-reference.com/players/w/westbru01/gamelog/2020.
    

* [`repl.it` Examples](https://repl.it/@jaebradley/RegularSeasonPlayerBoxScores#main.py)

=== "Python Data Structures"
    ```python
    from basketball_reference_web_scraper import client

    client.regular_season_player_box_scores(
        player_identifier="westbru01", 
        season_end_year=2018
    )
    ```
    
=== "JSON"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.regular_season_player_box_scores(
        player_identifier="westbru01", 
        season_end_year=2018, 
        output_type=OutputType.JSON
    )
    ```

=== "JSON to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.regular_season_player_box_scores(
        player_identifier="westbru01", 
        season_end_year=2018, 
        output_type=OutputType.JSON,
        output_file_path="./2017_2018_russell_westbrook_regular_season_box_scores.json"
    )
    ```
       
=== "CSV to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.regular_season_player_box_scores(
        player_identifier="westbru01", 
        season_end_year=2018, 
        output_type=OutputType.CSV, 
        output_file_path="./2017_2018_russell_westbrook_regular_season_box_scores.csv"
    )
    ```


### Playoff Player Box Scores

!!! note
    The `player_identifier` is **Basketball Reference's** unique identifier for each player. 
    
    In the case of Russell Westbrook, their `player_identifier` is **`westbru01`**.
    
    You can see this from their player page URL: https://www.basketball-reference.com/players/w/westbru01/gamelog/2020.
    

* [`repl.it` Examples](https://repl.it/@jaebradley/PlayoffPlayerBoxScores#main.py)

=== "Python Data Structures"
    ```python
    from basketball_reference_web_scraper import client

    client.playoff_player_box_scores(
        player_identifier="westbru01", 
        season_end_year=2018
    )
    ```
    
=== "JSON"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.playoff_player_box_scores(
        player_identifier="westbru01", 
        season_end_year=2018, 
        output_type=OutputType.JSON
    )
    ```

=== "JSON to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.playoff_player_box_scores(
        player_identifier="westbru01", 
        season_end_year=2018, 
        output_type=OutputType.JSON,
        output_file_path="./2017_2018_russell_westbrook_playoff_box_scores.json"
    )
    ```
       
=== "CSV to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.playoff_player_box_scores(
        player_identifier="westbru01", 
        season_end_year=2018, 
        output_type=OutputType.CSV, 
        output_file_path="./2017_2018_russell_westbrook_playoff_box_scores.csv"
    )
    ```
    
### Search

* [`repli.t` Examples](https://repl.it/@jaebradley/Search#main.py)

=== "Python Data Structures"
    ```python
    from basketball_reference_web_scraper import client

    client.search(term="Ko")
    ```
    
=== "JSON"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.search(term="Ko", output_type=OutputType.JSON)
    ```

=== "JSON to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.search(
        term="Ko",
        output_type=OutputType.JSON, 
        output_file_path="./1_1_2017_box_scores.json"
    )
    ```
       
=== "CSV to file"
    ```python
    from basketball_reference_web_scraper import client
    from basketball_reference_web_scraper.data import OutputType

    client.search(
        term="Ko",
        output_type=OutputType.CSV, 
        output_file_path="./1_1_2017_box_scores.csv"
    )
    ```

