from datetime import datetime
from unittest import TestCase

import basketball_reference_web_scraper.client as client
from basketball_reference_web_scraper.data import OutputWriteOption, OutputType


class TestClient(TestCase):
    def test_schedules_from_2001(self):
        now = datetime.now()
        current_year = now.year

        for year in range(2001, current_year + 1):
            season_schedule = client.season_schedule(season_end_year=year)
            self.assertIsNotNone(season_schedule)

    def test_output_json_box_scores_to_file(self):
        client.box_scores(
            day=1,
            month=1,
            year=2001,
            output_type=OutputType.JSON,
            output_file_path="./foo.json",
            output_write_option=OutputWriteOption.WRITE
        )

    def test_output_json_box_scores_to_memory(self):
        january_first_box_scores = client.box_scores(
            day=1,
            month=1,
            year=2001,
            output_type=OutputType.JSON,
        )

        self.assertIsNotNone(january_first_box_scores)

    def test_2018_player_season_totals(self):
        now = datetime.now()
        current_year = now.year

        for year in range(2001, current_year + 1):
            player_season_totals = client.player_season_totals(season_end_year=year)
            self.assertIsNotNone(player_season_totals)