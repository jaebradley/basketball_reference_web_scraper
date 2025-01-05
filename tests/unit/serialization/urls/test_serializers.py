import unittest
from datetime import date
from unittest import mock

from basketball_reference_web_scraper.data import TeamAbbreviation
from basketball_reference_web_scraper.serialization.urls.models import PlayByPlayURLData
from basketball_reference_web_scraper.serialization.urls.serializers import PlayByPlayURLSerializer, \
    DEFAULT_PLAY_BY_PLAY_URL_SERIALIZER


class TestPlayByPlayURLSerializer(unittest.TestCase):
    def setUp(self):
        self.serializer = PlayByPlayURLSerializer(
            date_serializer=mock.Mock(name="mock date serializer",
                                      serialize=mock.Mock(return_value="some serialized date")),
            team_abbreviation_serializer=mock.Mock(name="mock team abbreviation serializer", serialize=mock.Mock(
                return_value="some serialized team abbreviation"))
        )

        super().setUp()

    def test_output(self):
        self.assertEqual(
            "https://www.basketball-reference.com/boxscores/pbp/some serialized date0some serialized team abbreviation.html",
            self.serializer.serialize(value=PlayByPlayURLData(
                date=date(year=2001, month=1, day=1),
                team_abbreviation=TeamAbbreviation.BOS
            ))
        )


class TestDefaultPlayByPlayURLSerializer(unittest.TestCase):
    def test_output(self):
        self.assertEqual(
            "https://www.basketball-reference.com/boxscores/pbp/200101090CHH.html",
            DEFAULT_PLAY_BY_PLAY_URL_SERIALIZER.serialize(
                value=PlayByPlayURLData(
                    date=date(year=2001, month=1, day=9),
                    team_abbreviation=TeamAbbreviation.CHH
                ))
        )
