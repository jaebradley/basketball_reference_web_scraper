from unittest import TestCase, mock

from basketball_reference_web_scraper.data import OutputWriteOption
from basketball_reference_web_scraper.output.writers import JSONWriter


class TestJSONWriter(TestCase):
    def setUp(self):
        self.mock_encoder = mock.Mock()
        self.mock_data = ["some data"]
        self.writer = JSONWriter(value_formatter=self.mock_encoder)

    @mock.patch("json.dumps")
    def test_writing_to_memory_with_default_options(self, json_dumps):
        options = mock.Mock(
            formatting_options={},
            file_options=mock.Mock(
                path="some path",
                mode=OutputWriteOption.WRITE,
                should_write_to_file=False,
            ),
        )

        self.writer.write(data=self.mock_data, options=options)
        json_dumps.assert_called_once_with(
            self.mock_data,
            cls=self.mock_encoder,
            sort_keys=True,
            indent=4,
        )

    @mock.patch("json.dumps")
    def test_writing_to_memory_with_custom_options(self, json_dumps):
        options = mock.Mock(
            formatting_options={
                "jae": "baebae",
                "bae": "jadley",
            },
            file_options=mock.Mock(
                path="some path",
                mode=OutputWriteOption.WRITE,
                should_write_to_file=False,
            )
        )

        self.writer.write(data=self.mock_data, options=options)
        json_dumps.assert_called_once_with(
            self.mock_data,
            cls=self.mock_encoder,
            sort_keys=True,
            indent=4,
            jae="baebae",
            bae="jadley",
        )

    @mock.patch("json.dump")
    def test_writing_to_file_with_default_options(self, json_dump):
        with mock.patch("builtins.open", mock.mock_open()) as mock_file:
            options = mock.Mock(
                formatting_options={},
                file_options=mock.Mock(
                    path="some path",
                    mode=OutputWriteOption.WRITE,
                    should_write_to_file=True,
                ),
            )

            self.writer.write(data=self.mock_data, options=options)
            mock_file.assert_called_once_with("some path", OutputWriteOption.WRITE.value, newline="", encoding="utf8")
            json_dump.assert_called_once_with(
                self.mock_data,
                mock_file(),
                cls=self.mock_encoder,
                sort_keys=True,
                indent=4,
            )

    @mock.patch("json.dump")
    def test_writing_to_file_with_custom_options(self, json_dump):
        with mock.patch("builtins.open", mock.mock_open()) as mock_file:
            options = mock.Mock(
                formatting_options={
                    "jae": "baebae",
                    "bae": "jadley",
                },
                file_options=mock.Mock(
                    path="some path",
                    mode=OutputWriteOption.WRITE,
                    should_write_to_file=True,
                ),
            )
            self.writer.write(data=self.mock_data, options=options)
            mock_file.assert_called_once_with("some path", OutputWriteOption.WRITE.value, newline="", encoding="utf8")
            json_dump.assert_called_once_with(
                self.mock_data,
                mock_file(),
                cls=self.mock_encoder,
                sort_keys=True,
                indent=4,
                jae="baebae",
                bae="jadley",
            )
