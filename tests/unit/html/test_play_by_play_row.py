from unittest import TestCase
from unittest.mock import patch, PropertyMock, MagicMock

from basketball_reference_web_scraper.html import PlayByPlayRow


class TestPlayByPlayRow(TestCase):
    @patch.object(PlayByPlayRow, 'home_team_play_description', new_callable=PropertyMock)
    def test_is_home_team_play_when_home_team_play_description_is_not_empty_string(self, mocked_play_description):
        mocked_play_description.return_value = "jaebaebae"

        self.assertTrue(PlayByPlayRow(html=MagicMock()).is_home_team_play)

    @patch.object(PlayByPlayRow, 'home_team_play_description', new_callable=PropertyMock)
    def test_is_not_home_team_play_when_home_team_play_description_is_empty_string(self, mocked_play_description):
        mocked_play_description.return_value = ""

        self.assertFalse(PlayByPlayRow(html=MagicMock()).is_home_team_play)
