import os
import json
from unittest import TestCase

from basketball_reference_web_scraper.client import standings
from basketball_reference_web_scraper.data import Team, Division, Conference, OutputWriteOption, OutputType


class TestStandingsInMemory(TestCase):
    def test_2000_standings(self):
        result = standings(season_end_year=2000)
        self.assertEqual(len(result), 29)

        miami_heat = result[0]
        self.assertEqual(miami_heat["team"], Team.MIAMI_HEAT)
        self.assertEqual(miami_heat["wins"], 52)
        self.assertEqual(miami_heat["losses"], 30)
        self.assertEqual(miami_heat["division"], Division.ATLANTIC)
        self.assertEqual(miami_heat["conference"], Conference.EASTERN)

        los_angeles_clippers = result[28]
        self.assertEqual(los_angeles_clippers["team"], Team.LOS_ANGELES_CLIPPERS)
        self.assertEqual(los_angeles_clippers["wins"], 15)
        self.assertEqual(los_angeles_clippers["losses"], 67)
        self.assertEqual(los_angeles_clippers["division"], Division.PACIFIC)
        self.assertEqual(los_angeles_clippers["conference"], Conference.WESTERN)

    def test_2001_standings(self):
        result = standings(season_end_year=2001)
        self.assertEqual(len(result), 29)

        philadelphia_76ers = result[0]
        self.assertEqual(philadelphia_76ers["team"], Team.PHILADELPHIA_76ERS)
        self.assertEqual(philadelphia_76ers["wins"], 56)
        self.assertEqual(philadelphia_76ers["losses"], 26)
        self.assertEqual(philadelphia_76ers["division"], Division.ATLANTIC)
        self.assertEqual(philadelphia_76ers["conference"], Conference.EASTERN)

        golden_state_warriors = result[28]
        self.assertEqual(golden_state_warriors["team"], Team.GOLDEN_STATE_WARRIORS)
        self.assertEqual(golden_state_warriors["wins"], 17)
        self.assertEqual(golden_state_warriors["losses"], 65)
        self.assertEqual(golden_state_warriors["division"], Division.PACIFIC)
        self.assertEqual(golden_state_warriors["conference"], Conference.WESTERN)


def test_2002_standings(self):
    result = standings(season_end_year=2002)
    self.assertEqual(len(result), 30)

    philadelphia_76ers = result[0]
    self.assertEqual(philadelphia_76ers["team"], Team.PHILADELPHIA_76ERS)
    self.assertEqual(philadelphia_76ers["wins"], 56)
    self.assertEqual(philadelphia_76ers["losses"], 26)
    self.assertEqual(philadelphia_76ers["division"], Division.ATLANTIC)
    self.assertEqual(philadelphia_76ers["conference"], Conference.EASTERN)

    golden_state_warriors = result[29]
    self.assertEqual(golden_state_warriors["team"], Team.GOLDEN_STATE_WARRIORS)
    self.assertEqual(golden_state_warriors["wins"], 17)
    self.assertEqual(golden_state_warriors["losses"], 65)
    self.assertEqual(golden_state_warriors["division"], Division.PACIFIC)
    self.assertEqual(golden_state_warriors["conference"], Conference.WESTERN)


def test_2005_standings(self):
    result = standings(season_end_year=2005)
    self.assertEqual(len(result), 30)

    boston_celtics = result[0]
    self.assertEqual(boston_celtics["team"], Team.BOSTON_CELTICS)
    self.assertEqual(boston_celtics["wins"], 45)
    self.assertEqual(boston_celtics["losses"], 37)
    self.assertEqual(boston_celtics["division"], Division.ATLANTIC)
    self.assertEqual(boston_celtics["conference"], Conference.EASTERN)

    detroit_pistons = result[6]
    self.assertEqual(detroit_pistons["team"], Team.DETROIT_PISTONS)
    self.assertEqual(detroit_pistons["wins"], 54)
    self.assertEqual(detroit_pistons["losses"], 28)
    self.assertEqual(detroit_pistons["division"], Division.CENTRAL)
    self.assertEqual(detroit_pistons["conference"], Conference.EASTERN)

    miami_heat = result[10]
    self.assertEqual(miami_heat["team"], Team.MIAMI_HEAT)
    self.assertEqual(miami_heat["wins"], 59)
    self.assertEqual(miami_heat["losses"], 23)
    self.assertEqual(miami_heat["division"], Division.SOUTHEAST)
    self.assertEqual(miami_heat["conference"], Conference.EASTERN)

    seattle_supersonics = result[15]
    self.assertEqual(seattle_supersonics["team"], Team.SEATTLE_SUPERSONICS)
    self.assertEqual(seattle_supersonics["wins"], 52)
    self.assertEqual(seattle_supersonics["losses"], 30)
    self.assertEqual(seattle_supersonics["division"], Division.NORTHWEST)
    self.assertEqual(seattle_supersonics["conference"], Conference.WESTERN)

    phoenix_suns = result[20]
    self.assertEqual(phoenix_suns["team"], Team.PHOENIX_SUNS)
    self.assertEqual(phoenix_suns["wins"], 62)
    self.assertEqual(phoenix_suns["losses"], 20)
    self.assertEqual(phoenix_suns["division"], Division.PACIFIC)
    self.assertEqual(phoenix_suns["conference"], Conference.WESTERN)

    new_orleans_hornets = result[29]
    self.assertEqual(new_orleans_hornets["team"], Team.NEW_ORLEANS_HORNETS)
    self.assertEqual(new_orleans_hornets["wins"], 18)
    self.assertEqual(new_orleans_hornets["losses"], 64)
    self.assertEqual(new_orleans_hornets["division"], Division.SOUTHWEST)
    self.assertEqual(new_orleans_hornets["conference"], Conference.WESTERN)


def test_2020_standings(self):
    result = standings(season_end_year=2020)
    self.assertEqual(len(result), 30)

    toronto_raptors = result[0]
    self.assertEqual(toronto_raptors["team"], Team.TORONTO_RAPTORS)
    self.assertEqual(toronto_raptors["wins"], 58)
    self.assertEqual(toronto_raptors["losses"], 24)
    self.assertEqual(toronto_raptors["division"], Division.ATLANTIC)
    self.assertEqual(toronto_raptors["conference"], Conference.EASTERN)

    milwaukee_bucks = result[6]
    self.assertEqual(milwaukee_bucks["team"], Team.MILWAUKEE_BUCKS)
    self.assertEqual(milwaukee_bucks["wins"], 60)
    self.assertEqual(milwaukee_bucks["losses"], 22)
    self.assertEqual(milwaukee_bucks["division"], Division.CENTRAL)
    self.assertEqual(milwaukee_bucks["conference"], Conference.EASTERN)

    orlando_magic = result[10]
    self.assertEqual(orlando_magic["team"], Team.ORLANDO_MAGIC)
    self.assertEqual(orlando_magic["wins"], 42)
    self.assertEqual(orlando_magic["losses"], 40)
    self.assertEqual(orlando_magic["division"], Division.SOUTHEAST)
    self.assertEqual(orlando_magic["conference"], Conference.EASTERN)

    denver_nuggets = result[15]
    self.assertEqual(denver_nuggets["team"], Team.DENVER_NUGGETS)
    self.assertEqual(denver_nuggets["wins"], 54)
    self.assertEqual(denver_nuggets["losses"], 28)
    self.assertEqual(denver_nuggets["division"], Division.NORTHWEST)
    self.assertEqual(denver_nuggets["conference"], Conference.WESTERN)

    golden_state_warriors = result[20]
    self.assertEqual(golden_state_warriors["team"], Team.GOLDEN_STATE_WARRIORS)
    self.assertEqual(golden_state_warriors["wins"], 57)
    self.assertEqual(golden_state_warriors["losses"], 25)
    self.assertEqual(golden_state_warriors["division"], Division.PACIFIC)
    self.assertEqual(golden_state_warriors["conference"], Conference.WESTERN)

    dallas_mavericks = result[29]
    self.assertEqual(dallas_mavericks["team"], Team.DALLAS_MAVERICKS)
    self.assertEqual(dallas_mavericks["wins"], 33)
    self.assertEqual(dallas_mavericks["losses"], 49)
    self.assertEqual(dallas_mavericks["division"], Division.SOUTHWEST)
    self.assertEqual(dallas_mavericks["conference"], Conference.WESTERN)


class TestCSVStandingsFor2001(TestCase):
    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/2001_standings.csv",
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2001_standings.csv",
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def test_2001_standings(self):
        standings(
            season_end_year=2001,
            output_type=OutputType.CSV,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )
        with open(self.output_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(output_file.readlines(), expected_output_file.readlines())


class TestJSONPlayerBoxScores2001(TestCase):
    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/2001_standings.json",
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2001_standings.json",
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def test_2001_standings(self):
        standings(
            season_end_year=2001,
            output_type=OutputType.JSON,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )

        with open(self.output_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.load(output_file),
                json.load(expected_output_file),
            )


class TestInMemoryJSONStandings2001(TestCase):
    def setUp(self):
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2001_standings.json",
        )

    def test_2001_standings(self):
        box_scores = standings(
            season_end_year=2001,
            output_type=OutputType.JSON,
        )

        with open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.loads(box_scores),
                json.load(expected_output_file)
            )


class TestCSVStandingsFor2019(TestCase):
    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/2019_standings.csv",
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2019_standings.csv",
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def test_2019_standings(self):
        standings(
            season_end_year=2019,
            output_type=OutputType.CSV,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )
        with open(self.output_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(output_file.readlines(), expected_output_file.readlines())


class TestJSONPlayerBoxScores2019(TestCase):
    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/2019_standings.json",
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2019_standings.json",
        )

    def tearDown(self):
        os.remove(self.output_file_path)

    def test_2019_standings(self):
        standings(
            season_end_year=2019,
            output_type=OutputType.JSON,
            output_file_path=self.output_file_path,
            output_write_option=OutputWriteOption.WRITE,
        )

        with open(self.output_file_path, "r", encoding="utf8") as output_file, \
                open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.load(output_file),
                json.load(expected_output_file),
            )


class TestInMemoryJSONStandings2019(TestCase):
    def setUp(self):
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "../output/expected/2019_standings.json",
        )

    def test_2019_standings(self):
        box_scores = standings(
            season_end_year=2019,
            output_type=OutputType.JSON,
        )

        with open(self.expected_output_file_path, "r", encoding="utf8") as expected_output_file:
            self.assertEqual(
                json.loads(box_scores),
                json.load(expected_output_file)
            )

