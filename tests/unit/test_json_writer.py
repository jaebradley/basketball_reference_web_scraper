from unittest import TestCase, mock

from basketball_reference_web_scraper.data import OutputWriteOption
from basketball_reference_web_scraper.writers import JSONWriter


class TestJSONWriter(TestCase):
    def setUp(self):
        self.mock_encoder = mock.Mock()
        self.mock_data = ["some data"]
        self.writer = JSONWriter(encoder=self.mock_encoder)

    def test_default_options(self):
        self.assertEqual({"sort_keys": True, "indent": 4}, JSONWriter.DEFAULT_OPTIONS)

    @mock.patch("basketball_reference_web_scraper.writers.json.dumps")
    def test_writing_to_memory_with_default_options(self, json_dumps):
        options = mock.Mock(
            custom_options=None,
            should_write_to_file=mock.Mock(return_value=False),
        )

        self.writer.write(data=self.mock_data, options=options)
        options.should_write_to_file.assert_called_once_with()
        json_dumps.assert_called_once_with(self.mock_data, cls=self.mock_encoder, sort_keys=True, indent=4)

    @mock.patch("basketball_reference_web_scraper.writers.json.dumps")
    def test_writing_to_memory_with_custom_options(self, json_dumps):
        options = mock.Mock(
            custom_options={
                "jae": "baebae",
                "bae": "jadley",
            },
            should_write_to_file=mock.Mock(return_value=False),
        )

        self.writer.write(data=self.mock_data, options=options)
        options.should_write_to_file.assert_called_once_with()
        json_dumps.assert_called_once_with(
            self.mock_data,
            cls=self.mock_encoder,
            sort_keys=True,
            indent=4,
            jae="baebae",
            bae="jadley",
        )

    @mock.patch("basketball_reference_web_scraper.writers.json.dump")
    def test_writing_to_file_with_default_options(self, json_dump):
        file_path = "some file path"
        with mock.patch("builtins.open", mock.mock_open()) as mock_file:
            options = mock.Mock(
                file_path=file_path,
                mode=OutputWriteOption.WRITE,
                custom_options=None,
                should_write_to_file=mock.Mock(return_value=True),
            )

            self.writer.write(data=self.mock_data, options=options)
            options.should_write_to_file.assert_called_once_with()
            mock_file.assert_called_once_with(file_path, OutputWriteOption.WRITE.value, newline="", encoding="utf8")
            json_dump.assert_called_once_with(
                self.mock_data,
                mock_file(),
                cls=self.mock_encoder,
                sort_keys=True,
                indent=4,
            )

    @mock.patch("basketball_reference_web_scraper.writers.json.dump")
    def test_writing_to_file_with_custom_options(self, json_dump):
        file_path = "some file path"
        with mock.patch("builtins.open", mock.mock_open()) as mock_file:
            options = mock.Mock(
                file_path=file_path,
                mode=OutputWriteOption.WRITE,
                custom_options={
                    "jae": "baebae",
                    "bae": "jadley",
                },
                should_write_to_file=mock.Mock(return_value=True),
            )

            self.writer.write(data=self.mock_data, options=options)
            options.should_write_to_file.assert_called_once_with()
            mock_file.assert_called_once_with(file_path, OutputWriteOption.WRITE.value, newline="", encoding="utf8")
            json_dump.assert_called_once_with(
                self.mock_data,
                mock_file(),
                cls=self.mock_encoder,
                sort_keys=True,
                indent=4,
                jae="baebae",
                bae="jadley",
            )
