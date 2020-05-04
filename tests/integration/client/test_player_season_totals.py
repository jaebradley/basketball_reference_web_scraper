import json
import os
from unittest import TestCase

from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Position, Team, OutputType


class BaseTestPlayerAdvancedSeasonTotalsCSVOutput(TestCase):
    @property
    def year(self):
        raise NotImplementedError

    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/player_season_totals_{year}.csv".format(year=self.year),
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/player_season_totals_{year}.csv".format(year=self.year),
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def assert_csv(self):
        client.players_season_totals(
            season_end_year=self.year,
            output_type=OutputType.CSV,
            output_file_path=self.output_file_path,
        )

        with open(self.output_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                output_file.readlines(),
                expected_output_file.readlines(),
            )


class BaseTestPlayerAdvancedSeasonTotalsJSONOutput(TestCase):
    @property
    def year(self):
        raise NotImplementedError

    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/player_season_totals_{year}.json".format(year=self.year),
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/player_season_totals_{year}.json".format(year=self.year),
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def assert_json(self):
        client.players_season_totals(
            season_end_year=self.year,
            output_type=OutputType.JSON,
            output_file_path=self.output_file_path,
        )

        with open(self.output_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.load(output_file),
                json.load(expected_output_file),
            )


class BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput(TestCase):
    @property
    def year(self):
        raise NotImplementedError

    def setUp(self):
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/player_season_totals_{year}.json".format(year=self.year),
        )

    def assert_json(self):
        results = client.players_season_totals(
            season_end_year=self.year,
            output_type=OutputType.JSON,
        )

        with open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.loads(results),
                json.load(expected_output_file),
            )


class Test2001PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2001

    def test_2001_csv_output(self):
        self.assert_csv()


class Test2002PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2002

    def test_2002_csv_output(self):
        self.assert_csv()


class Test2003PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2003

    def test_2003_csv_output(self):
        self.assert_csv()


class Test2004PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2004

    def test_2004_csv_output(self):
        self.assert_csv()


class Test2005PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2005

    def test_2005_csv_output(self):
        self.assert_csv()


class Test2006PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2006

    def test_2006_csv_output(self):
        self.assert_csv()


class Test2007PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2007

    def test_2007_csv_output(self):
        self.assert_csv()


class Test2008PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2008

    def test_2008_csv_output(self):
        self.assert_csv()


class Test2009PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2009

    def test_2009_csv_output(self):
        self.assert_csv()


class Test2010PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2010

    def test_2010_csv_output(self):
        self.assert_csv()


class Test2011PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2011

    def test_2011_csv_output(self):
        self.assert_csv()


class Test2012PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2012

    def test_2012_csv_output(self):
        self.assert_csv()


class Test2013PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2013

    def test_2013_csv_output(self):
        self.assert_csv()


class Test2014PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2014

    def test_2014_csv_output(self):
        self.assert_csv()


class Test2015PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2015

    def test_2015_csv_output(self):
        self.assert_csv()


class Test2016PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2016

    def test_2016_csv_output(self):
        self.assert_csv()


class Test2017PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2017

    def test_2017_csv_output(self):
        self.assert_csv()


class Test2018PlayerSeasonCSVTotals(BaseTestPlayerAdvancedSeasonTotalsCSVOutput):
    @property
    def year(self):
        return 2018

    def test_2018_csv_output(self):
        self.assert_csv()


class Test2001PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2001

    def test_2001_json_output(self):
        self.assert_json()


class Test2002PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2002

    def test_2002_json_output(self):
        self.assert_json()


class Test2003PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2003

    def test_2003_json_output(self):
        self.assert_json()


class Test2004PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2004

    def test_2004_json_output(self):
        self.assert_json()


class Test2005PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2005

    def test_2005_json_output(self):
        self.assert_json()


class Test2006PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2006

    def test_2006_json_output(self):
        self.assert_json()


class Test2007PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2007

    def test_2007_json_output(self):
        self.assert_json()


class Test2008PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2008

    def test_2008_json_output(self):
        self.assert_json()


class Test2009PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2009

    def test_2009_json_output(self):
        self.assert_json()


class Test2010PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2010

    def test_2010_json_output(self):
        self.assert_json()


class Test2011PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2011

    def test_2011_json_output(self):
        self.assert_json()


class Test2012PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2012

    def test_2012_json_output(self):
        self.assert_json()


class Test2013PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2013

    def test_2013_json_output(self):
        self.assert_json()


class Test2014PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2014

    def test_2014_json_output(self):
        self.assert_json()


class Test2015PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2015

    def test_2015_json_output(self):
        self.assert_json()


class Test2016PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2016

    def test_2016_json_output(self):
        self.assert_json()


class Test2017PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2017

    def test_2017_json_output(self):
        self.assert_json()


class Test2018PlayerSeasonJSONTotals(BaseTestPlayerAdvancedSeasonTotalsJSONOutput):
    @property
    def year(self):
        return 2018

    def test_2018_json_output(self):
        self.assert_json()


class Test2001PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2001

    def test_2001_json_output(self):
        self.assert_json()


class Test2002PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2002

    def test_2002_json_output(self):
        self.assert_json()


class Test2003PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2003

    def test_2003_json_output(self):
        self.assert_json()


class Test2004PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2004

    def test_2004_json_output(self):
        self.assert_json()


class Test2005PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2005

    def test_2005_json_output(self):
        self.assert_json()


class Test2006PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2006

    def test_2006_json_output(self):
        self.assert_json()


class Test2007PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2007

    def test_2007_json_output(self):
        self.assert_json()


class Test2008PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2008

    def test_2008_json_output(self):
        self.assert_json()


class Test2009PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2009

    def test_2009_json_output(self):
        self.assert_json()


class Test2010PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2010

    def test_2010_json_output(self):
        self.assert_json()


class Test2011PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2011

    def test_2011_json_output(self):
        self.assert_json()


class Test2012PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2012

    def test_2012_json_output(self):
        self.assert_json()


class Test2013PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2013

    def test_2013_json_output(self):
        self.assert_json()


class Test2014PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2014

    def test_2014_json_output(self):
        self.assert_json()


class Test2015PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2015

    def test_2015_json_output(self):
        self.assert_json()


class Test2016PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2016

    def test_2016_json_output(self):
        self.assert_json()


class Test2017PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2017

    def test_2017_json_output(self):
        self.assert_json()


class Test2018PlayerSeasonInMemoryJSONTotals(BaseTestPlayerAdvancedSeasonTotalsInMemoryJSONOutput):
    @property
    def year(self):
        return 2018

    def test_2018_json_output(self):
        self.assert_json()


class TestInMemoryPlayerSeasonTotals(TestCase):
    def test_2001_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2001)
        self.assertEqual(len(player_season_totals), 490)

    def test_first_2001_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2001)
        self.assertEqual(
            player_season_totals[0],
            {
                "slug": "abdulma02",
                "name": "Mahmoud Abdul-Rauf",
                "positions": [Position.POINT_GUARD],
                "age": 31,
                "team": Team.VANCOUVER_GRIZZLIES,
                "games_played": 41,
                "games_started": 0,
                "minutes_played": 486,
                "made_field_goals": 120,
                "attempted_field_goals": 246,
                "made_three_point_field_goals": 4,
                "attempted_three_point_field_goals": 14,
                "made_free_throws": 22,
                "attempted_free_throws": 29,
                "offensive_rebounds": 5,
                "defensive_rebounds": 20,
                "assists": 76,
                "steals": 9,
                "blocks": 1,
                "turnovers": 26,
                "personal_fouls": 50,
                "points": 266,
            }
        )

    def test_last_2001_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2001)
        self.assertEqual(
            player_season_totals[len(player_season_totals) - 1],
            {
                "slug": "zhizhwa01",
                "name": "Wang Zhizhi",
                "positions": [Position.CENTER],
                "age": 23,
                "team": Team.DALLAS_MAVERICKS,
                "games_played": 5,
                "games_started": 0,
                "minutes_played": 38,
                "made_field_goals": 8,
                "attempted_field_goals": 19,
                "made_three_point_field_goals": 0,
                "attempted_three_point_field_goals": 2,
                "made_free_throws": 8,
                "attempted_free_throws": 10,
                "offensive_rebounds": 1,
                "defensive_rebounds": 6,
                "assists": 0,
                "steals": 0,
                "blocks": 0,
                "turnovers": 1,
                "personal_fouls": 8,
                "points": 24,
            }
        )

    def test_2002_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2002)
        self.assertEqual(len(player_season_totals), 470)

    def test_2003_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2003)
        self.assertEqual(len(player_season_totals), 456)

    def test_2004_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2004)
        self.assertEqual(len(player_season_totals), 517)

    def test_2005_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2005)
        self.assertEqual(len(player_season_totals), 526)

    def test_2006_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2006)
        self.assertEqual(len(player_season_totals), 512)

    def test_2007_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2007)
        self.assertEqual(len(player_season_totals), 487)

    def test_2008_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2008)
        self.assertEqual(len(player_season_totals), 527)

    def test_2009_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2009)
        self.assertEqual(len(player_season_totals), 515)

    def test_2010_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2010)
        self.assertEqual(len(player_season_totals), 512)

    def test_2011_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2011)
        self.assertEqual(len(player_season_totals), 542)

    def test_2012_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2012)
        self.assertEqual(len(player_season_totals), 515)

    def test_2013_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2013)
        self.assertEqual(len(player_season_totals), 523)

    def test_2014_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2014)
        self.assertEqual(len(player_season_totals), 548)

    def test_2015_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2015)
        self.assertEqual(len(player_season_totals), 575)

    def test_2016_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2016)
        self.assertEqual(len(player_season_totals), 528)

    def test_2017_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2017)
        self.assertEqual(len(player_season_totals), 542)

    def test_2018_player_season_totals_length(self):
        player_season_totals = client.players_season_totals(season_end_year=2018)
        self.assertEqual(len(player_season_totals), 605)

    def test_2019_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2019)
        self.assertEqual(len(player_season_totals), 622)

    def test_avery_bradley_2019_player_season_totals(self):
        player_season_totals = client.players_season_totals(season_end_year=2019)
        clippers_avery_bradley = player_season_totals[66]

        self.assertEqual('bradlav01', clippers_avery_bradley["slug"])
        self.assertEqual("Avery Bradley", clippers_avery_bradley["name"])
        self.assertListEqual([Position.SHOOTING_GUARD], clippers_avery_bradley["positions"])
        self.assertEqual(28, clippers_avery_bradley["age"])
        self.assertEqual(Team.LOS_ANGELES_CLIPPERS, clippers_avery_bradley["team"])
        self.assertEqual(49, clippers_avery_bradley["games_played"])
        self.assertEqual(49, clippers_avery_bradley["games_started"])
        self.assertEqual(1463, clippers_avery_bradley["minutes_played"])
        self.assertEqual(161, clippers_avery_bradley["made_field_goals"])
        self.assertEqual(420, clippers_avery_bradley["attempted_field_goals"])
        self.assertEqual(58, clippers_avery_bradley["made_three_point_field_goals"])
        self.assertEqual(172, clippers_avery_bradley["attempted_three_point_field_goals"])
        self.assertEqual(20, clippers_avery_bradley["made_free_throws"])
        self.assertEqual(25, clippers_avery_bradley["attempted_free_throws"])
        self.assertEqual(35, clippers_avery_bradley["offensive_rebounds"])
        self.assertEqual(96, clippers_avery_bradley["defensive_rebounds"])
        self.assertEqual(96, clippers_avery_bradley["assists"])
        self.assertEqual(27, clippers_avery_bradley["steals"])
        self.assertEqual(16, clippers_avery_bradley["blocks"])
        self.assertEqual(61, clippers_avery_bradley["turnovers"])
        self.assertEqual(133, clippers_avery_bradley["personal_fouls"])
        self.assertEqual(400, clippers_avery_bradley["points"])
