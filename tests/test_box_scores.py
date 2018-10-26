from unittest import TestCase

from client import box_scores
from data import OutputType


class TestBox_scores(TestCase):
    def test_get_box_scores(self):
        result = box_scores(day=1, month=1, year=2018, output_type=OutputType.JSON)
        self.assertIsNotNone(result)

    def test_get_box_scores_to_csv(self):
        box_scores(day=1, month=1, year=2018, output_type=OutputType.CSV, relative_file_path="./foo.csv")