from unittest import TestCase

from basketball_reference_web_scraper.data import OUTCOME_ABBREVIATIONS_TO_OUTCOME, Outcome
from basketball_reference_web_scraper.parsers import OutcomeAbbreviationParser, PlayerBoxScoreOutcomeParser


class TestPlayerBoxScoreOutcomeParser(TestCase):
    def setUp(self):
        self.parser = PlayerBoxScoreOutcomeParser(
            outcome_abbreviation_parser=OutcomeAbbreviationParser(
                abbreviations_to_outcomes=OUTCOME_ABBREVIATIONS_TO_OUTCOME
            )
        )

    def test_parse_win_abbreviation_for_single_digit_margin_of_victory(self):
        self.assertEqual("W", self.parser.parse_outcome_abbreviation(formatted_outcome="W, (1, 0)"))
