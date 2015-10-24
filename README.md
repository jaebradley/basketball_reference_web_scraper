# Basketball Reference Web Scraper
[Basketball Reference](http://www.basketball-reference.com) is a great site (especially for a basketball stats nut like me), and hopefully they don't get too pissed off at me for creating this.

Basically, I created this repository as a utility for another project where I'm trying to estimate an NBA player's productivity as it relates to daily fantasy sports.  For that project, I need box score and scheduling information, which is provided by this utility.

## Getting Box Scores
There are two methods that return box scores for a given date:

* `BoxScoreWebScraper.return_box_scores_for_date(date)`
  * Returns a list of Box Score objects
* `BoxScoreWebScraper.return_json_encoded_box_scores_for_date(date)`
  * Returns a JSON object representation of a list of Box Score objects

## Getting Season Schedule Information
There are also two methods that return scheduling information for a given season start year (note that the NBA season generally spans two calendar years):

* `SeasonScheduleWebScraper.return_schedule(season_start_year)`
  * Returns a Schedule object
* `SeasonScheduleWebScraper.return_json_encoded_schedule(season_start_year)`
  * Returns a JSON representation of a Schedule object
