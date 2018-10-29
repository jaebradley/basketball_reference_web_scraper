from unittest import TestCase

from datetime import datetime
import logging

import basketball_reference_web_scraper.client as client
from basketball_reference_web_scraper.data import Outcome, Team
from basketball_reference_web_scraper.parsers import box_scores


class TestClient(TestCase):
    def test_schedules_from_2001(self):
        now = datetime.now()
        current_year = now.year

        for year in range(2001, current_year + 1):
            season_schedule = client.season_schedule(season_end_year=year)
            self.assertIsNotNone(season_schedule)
