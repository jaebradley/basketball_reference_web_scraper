import filecmp
import functools
import json
import os
from unittest import TestCase

import requests_mock

from basketball_reference_web_scraper.client import standings
from basketball_reference_web_scraper.data import Team, Division, Conference, OutputWriteOption, OutputType


class StandingsMocker:
    def __init__(self, schedules_directory, season_end_year):
        self._schedules_directory = schedules_directory
        self._season_end_year = season_end_year

    def decorate_class(self, klass):
        for attr_name in dir(klass):
            if not attr_name.startswith('test_'):
                continue

            attr = getattr(klass, attr_name)
            if not hasattr(attr, '__call__'):
                continue

            setattr(klass, attr_name, self.mock(attr))

        return klass

    def mock(self, callable):
        @functools.wraps(callable)
        def inner(*args, **kwargs):
            html_files_directory = os.path.join(self._schedules_directory, str(self._season_end_year))
            for file in os.listdir(os.fsencode(html_files_directory)):
                filename = os.fsdecode(file)
                if not filename.endswith(".html"):
                    raise ValueError(
                        f"Unexpected prefix for {filename}. Expected all files in {html_files_directory} to end with .html.")

                with open(os.path.join(html_files_directory, filename), 'r') as file_input:
                    if filename.startswith(str(self._season_end_year)):
                        key = f"https://www.basketball-reference.com/leagues/NBA_{self._season_end_year}_games.html"
                        with requests_mock.Mocker() as m:
                            m.get(key, text=file_input.read(), status_code=200)

            return callable(*args, **kwargs)

        return inner

    def __call__(self, obj):
        if isinstance(obj, type):
            return self.decorate_class(obj)

        raise ValueError("Should only be used as a class decorator")


@StandingsMocker(
    schedules_directory=os.path.join(
        os.path.dirname(__file__),
        "../files/schedule",
    ),
    season_end_year=2000
)
class Test2000StandingsInMemory(TestCase):
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


@StandingsMocker(
    schedules_directory=os.path.join(
        os.path.dirname(__file__),
        "../files/schedule",
    ),
    season_end_year=2001
)
class Test2001StandingsInMemory(TestCase):

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


@StandingsMocker(
    schedules_directory=os.path.join(
        os.path.dirname(__file__),
        "../files/schedule",
    ),
    season_end_year=2002
)
class Test2002StandingsInMemory(TestCase):
    def test_2002_standings(self):
        result = standings(season_end_year=2002)
        self.assertEqual(len(result), 29)

        nets = result[0]
        self.assertEqual(nets["team"], Team.NEW_JERSEY_NETS)
        self.assertEqual(nets["wins"], 52)
        self.assertEqual(nets["losses"], 30)
        self.assertEqual(nets["division"], Division.ATLANTIC)
        self.assertEqual(nets["conference"], Conference.EASTERN)

        golden_state_warriors = result[28]
        self.assertEqual(golden_state_warriors["team"], Team.GOLDEN_STATE_WARRIORS)
        self.assertEqual(golden_state_warriors["wins"], 21)
        self.assertEqual(golden_state_warriors["losses"], 61)
        self.assertEqual(golden_state_warriors["division"], Division.PACIFIC)
        self.assertEqual(golden_state_warriors["conference"], Conference.WESTERN)


@StandingsMocker(
    schedules_directory=os.path.join(
        os.path.dirname(__file__),
        "../files/schedule",
    ),
    season_end_year=2005
)
class Test2005StandingsInMemory(TestCase):
    def test_2005_standings(self):
        result = standings(season_end_year=2005)
        self.assertEqual(len(result), 30)

        phoenix_suns = result[0]
        self.assertEqual(phoenix_suns["team"], Team.BOSTON_CELTICS)
        self.assertEqual(phoenix_suns["wins"], 45)
        self.assertEqual(phoenix_suns["losses"], 37)
        self.assertEqual(phoenix_suns["division"], Division.ATLANTIC)
        self.assertEqual(phoenix_suns["conference"], Conference.EASTERN)

        detroit_pistons = result[5]
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


@StandingsMocker(
    schedules_directory=os.path.join(
        os.path.dirname(__file__),
        "../files/schedule",
    ),
    season_end_year=2020
)
class Test2020StandingsInMemory(TestCase):
    def test_2020_standings(self):
        result = standings(season_end_year=2020)
        self.assertEqual(len(result), 30)

        toronto_raptors = result[0]
        self.assertEqual(toronto_raptors["team"], Team.TORONTO_RAPTORS)
        self.assertEqual(toronto_raptors["wins"], 53)
        self.assertEqual(toronto_raptors["losses"], 19)
        self.assertEqual(toronto_raptors["division"], Division.ATLANTIC)
        self.assertEqual(toronto_raptors["conference"], Conference.EASTERN)

        milwaukee_bucks = result[5]
        self.assertEqual(milwaukee_bucks["team"], Team.MILWAUKEE_BUCKS)
        self.assertEqual(milwaukee_bucks["wins"], 56)
        self.assertEqual(milwaukee_bucks["losses"], 17)
        self.assertEqual(milwaukee_bucks["division"], Division.CENTRAL)
        self.assertEqual(milwaukee_bucks["conference"], Conference.EASTERN)

        orlando_magic = result[11]
        self.assertEqual(orlando_magic["team"], Team.ORLANDO_MAGIC)
        self.assertEqual(orlando_magic["wins"], 33)
        self.assertEqual(orlando_magic["losses"], 40)
        self.assertEqual(orlando_magic["division"], Division.SOUTHEAST)
        self.assertEqual(orlando_magic["conference"], Conference.EASTERN)

        denver_nuggets = result[15]
        self.assertEqual(denver_nuggets["team"], Team.DENVER_NUGGETS)
        self.assertEqual(denver_nuggets["wins"], 46)
        self.assertEqual(denver_nuggets["losses"], 27)
        self.assertEqual(denver_nuggets["division"], Division.NORTHWEST)
        self.assertEqual(denver_nuggets["conference"], Conference.WESTERN)

        golden_state_warriors = result[24]
        self.assertEqual(golden_state_warriors["team"], Team.GOLDEN_STATE_WARRIORS)
        self.assertEqual(golden_state_warriors["wins"], 15)
        self.assertEqual(golden_state_warriors["losses"], 50)
        self.assertEqual(golden_state_warriors["division"], Division.PACIFIC)
        self.assertEqual(golden_state_warriors["conference"], Conference.WESTERN)

        dallas_mavericks = result[26]
        self.assertEqual(dallas_mavericks["team"], Team.DALLAS_MAVERICKS)
        self.assertEqual(dallas_mavericks["wins"], 43)
        self.assertEqual(dallas_mavericks["losses"], 32)
        self.assertEqual(dallas_mavericks["division"], Division.SOUTHWEST)
        self.assertEqual(dallas_mavericks["conference"], Conference.WESTERN)


@StandingsMocker(
    schedules_directory=os.path.join(
        os.path.dirname(__file__),
        "../files/schedule",
    ),
    season_end_year=2001
)
class TestCSVStandingsFor2001(TestCase):
    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/standings/2001.csv"
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/standings/2001.csv"
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
        self.assertTrue(
            filecmp.cmp(
                self.output_file_path,
                self.expected_output_file_path))


@StandingsMocker(
    schedules_directory=os.path.join(
        os.path.dirname(__file__),
        "../files/schedule",
    ),
    season_end_year=2001
)
class TestJSONPlayerBoxScores2001(TestCase):
    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/standings/2001.json"
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/standings/2001.json"
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

        self.assertTrue(
            filecmp.cmp(
                self.output_file_path,
                self.expected_output_file_path))


@StandingsMocker(
    schedules_directory=os.path.join(
        os.path.dirname(__file__),
        "../files/schedule",
    ),
    season_end_year=2001
)
class TestInMemoryJSONStandings2001(TestCase):
    def setUp(self):
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/standings/2001.json"
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


@StandingsMocker(
    schedules_directory=os.path.join(
        os.path.dirname(__file__),
        "../files/schedule",
    ),
    season_end_year=2019
)
class TestCSVStandingsFor2019(TestCase):
    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/standings/2019.csv"
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/standings/2019.csv"
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
        self.assertTrue(
            filecmp.cmp(
                self.output_file_path,
                self.expected_output_file_path))


@StandingsMocker(
    schedules_directory=os.path.join(
        os.path.dirname(__file__),
        "../files/schedule",
    ),
    season_end_year=2019
)
class TestJSONPlayerBoxScores2019(TestCase):
    def setUp(self):
        self.output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/generated/standings/2019.json"
        )
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/standings/2019.json"
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

        self.assertTrue(
            filecmp.cmp(
                self.output_file_path,
                self.expected_output_file_path))


@StandingsMocker(
    schedules_directory=os.path.join(
        os.path.dirname(__file__),
        "../files/schedule",
    ),
    season_end_year=2019
)
class TestInMemoryJSONStandings2019(TestCase):
    def setUp(self):
        self.expected_output_file_path = os.path.join(
            os.path.dirname(__file__),
            "./output/expected/standings/2019.json"
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
