import os

import pytest

from basketball_reference_web_scraper import diagnostics


@pytest.fixture(scope="session", autouse=True)
def _offline_diagnostics_directory(tmp_path_factory):
    """Keep test runs from writing evidence into the developer's home journal.

    Diagnostics tests re-enable journaling explicitly with their own directory.
    """
    directory = tmp_path_factory.mktemp("diagnostics-disabled")
    os.environ["BASKETBALL_REFERENCE_DIAGNOSTICS"] = "off"
    os.environ["BASKETBALL_REFERENCE_DIAGNOSTICS_DIR"] = str(directory)
    yield
    os.environ.pop("BASKETBALL_REFERENCE_DIAGNOSTICS", None)
    os.environ.pop("BASKETBALL_REFERENCE_DIAGNOSTICS_DIR", None)


@pytest.fixture(autouse=True)
def _reset_diagnostics_state():
    diagnostics.reset()
    yield
    diagnostics.reset()
