import functools
import os
from typing import Dict

import requests_mock


class ResponseMocker:
    def __init__(self, basketball_reference_paths_by_filename: Dict[str, str]):
        self._basketball_reference_paths_by_filename = basketball_reference_paths_by_filename

    def decorate_class(self, klass):
        for attr_name in dir(klass):
            if not attr_name.startswith('test_'):
                continue

            attr = getattr(klass, attr_name)
            if not hasattr(attr, '__call__'):
                continue

            setattr(klass, attr_name, self.mock(attr))

        return klass

    def mock(self, callable):
        @functools.wraps(callable)
        def inner(*args, **kwargs):
            with requests_mock.Mocker() as m:
                for filename, basketball_reference_path in self._basketball_reference_paths_by_filename.items():
                    if not filename.endswith(".html"):
                        raise ValueError(
                            f"Unexpected prefix for {filename}. Expected all files in to end with .html.")

                    with open(filename, 'r') as file_input:
                        m.get(f"https://www.basketball-reference.com/{basketball_reference_path}",
                              text=file_input.read(),
                              status_code=200)
                return callable(*args, **kwargs)

        return inner

    def __call__(self, obj):
        if isinstance(obj, type):
            return self.decorate_class(obj)

        raise ValueError("Should only be used as a class decorator")


class SeasonScheduleMocker(ResponseMocker):
    def __init__(self, schedules_directory: str, season_end_year: int):
        basketball_reference_paths_by_filename: Dict[str, str] = {}
        html_files_directory = os.path.join(schedules_directory, str(season_end_year))
        for file in os.listdir(os.fsencode(html_files_directory)):
            filename = os.fsdecode(file)
            if filename.startswith(str(season_end_year)):
                key = f"leagues/NBA_{season_end_year}_games.html"
            else:
                key = f"leagues/NBA_{season_end_year}_games-{filename}"
            basketball_reference_paths_by_filename[os.path.join(html_files_directory, filename)] = key

        super().__init__(basketball_reference_paths_by_filename=basketball_reference_paths_by_filename)
