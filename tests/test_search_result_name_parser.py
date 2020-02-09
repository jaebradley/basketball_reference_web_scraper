from unittest import TestCase

from basketball_reference_web_scraper.parsers import SearchResultNameParser


class TestSearchResultNameParser(TestCase):
    def setUp(self):
        self.parser = SearchResultNameParser()

    def test_parse_name_with_parentheses_with_start_and_end_year(self):
        self.assertEqual(
            self.parser.parse(search_result_name='Kobe Bryant (1997-2016)'),
            'Kobe Bryant',
        )

    def test_parse_name_with_parentheses_with_start_year(self):
        self.assertEqual(
            self.parser.parse(search_result_name='Bud Koper (1965)'),
            'Bud Koper',
        )

    def test_parse_name_without_parentheses(self):
        self.assertEqual(
            self.parser.parse(search_result_name='Bronson Koenig'),
            'Bronson Koenig',
        )

