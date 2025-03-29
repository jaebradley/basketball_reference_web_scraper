import hashlib
import itertools
from decimal import Decimal
from unittest import TestCase

from basketball_reference_web_scraper.contracts.data.models import Salary
from basketball_reference_web_scraper.contracts.data.parsers import deserialize_season_start_year, deserialize_team, \
    deserialize_guaranteed_salary, SalariesBySeasonParser
from basketball_reference_web_scraper.data import Team


class TestDeserializingSeasonStartYear(TestCase):
    def test_non_numeric_value_raises_error(self):
        with self.assertRaises(ValueError):
            deserialize_season_start_year(serialized_season="foobar")

    def test_invalidly_formatted_numeric_value_raises_error(self):
        with self.assertRaises(ValueError):
            deserialize_season_start_year(serialized_season="2024")

    def test_validly_formatted_value_returns_value(self):
        assert 2024 == deserialize_season_start_year(serialized_season="2024-25")


class TestDeserializingTeamAbbreviation(TestCase):
    def test_invalid_abbreviation_raises_error(self):
        with self.assertRaisesRegexp(ValueError, "Unable to deserialize team abbreviation: jaebaebae"):
            deserialize_team("jaebaebae")

    def test_valid_abbreviation_returns_team(self):
        assert Team.BOSTON_CELTICS == deserialize_team("BOS")


class TestDeserializingGuaranteedSalary(TestCase):
    def test_raise_error_guaranteed_salary_column_does_not_exist(self):
        with self.assertRaises(ValueError):
            deserialize_guaranteed_salary(contract_values_by_column_identifier={})

    def test_raises_when_column_exists_but_value_is_an_empty_string(self):
        with self.assertRaises(ValueError):
            deserialize_guaranteed_salary(contract_values_by_column_identifier={"remain_gtd": ""})

    def test_returns_salary_when_column_exists_and_value_is_not_an_empty_string(self):
        assert Salary(amount=Decimal(1_234_567), currency="$") == deserialize_guaranteed_salary(
            contract_values_by_column_identifier={"remain_gtd": "$1,234,567"}
        )


class TestSalariesBySeasonParser(TestCase):
    def test_valid_salaries_by_season(self):
        def generate_salary():
            for value in itertools.count(start=0, step=1):
                yield Salary(amount=Decimal(value), currency="$")

        salary_generator = generate_salary()
        parser = SalariesBySeasonParser(
            season_start_year_deserializer=lambda v: int.from_bytes(hashlib.md5(v.encode("utf-8")).digest()[:8],
                                                                    'little', signed=True),
            salary_deserializer=lambda v: None if v is None else next(salary_generator)
        )
        assert {6699318081062747564: Salary(amount=Decimal('0'), currency='$'),
                -2012135647395072713: Salary(amount=Decimal('1'), currency='$')} == parser.parse(
            contract_values_by_column_identifier={
                "f": "bar",
                "b": "jae",
                "remain_gtd": "test"
            },
            column_names_by_identifier={
                "f": "foo",
                "b": "bar",
                "remain_gtd": "guaranteed_money"
            }
        )
