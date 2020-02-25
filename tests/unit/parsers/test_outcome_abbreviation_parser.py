from unittest import TestCase

from basketball_reference_web_scraper.data import Outcome, OUTCOME_ABBREVIATIONS_TO_OUTCOME
from basketball_reference_web_scraper.parsers import OutcomeAbbreviationParser


class TestOutcomeAbbreviationParser(TestCase):
    def setUp(self):
        self.parser = OutcomeAbbreviationParser(abbreviations_to_outcomes=OUTCOME_ABBREVIATIONS_TO_OUTCOME)

    def test_parse_unknown_outcome_symbol(self):
        self.assertRaises(ValueError, self.parser.from_abbreviation, "jaebaebae")

    def test_parse_win(self):
        self.assertEqual(Outcome.WIN, self.parser.from_abbreviation("W"))

    def test_parse_loss(self):
        self.assertEqual(Outcome.LOSS, self.parser.from_abbreviation("L"))
