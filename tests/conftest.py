import flask
import pathlib
import pytest
import tempfile

from appetiser import appetiser


@pytest.fixture
def appetiser_client() -> flask.Flask:
    appetiser.config["TESTING"] = True
    client = appetiser.test_client()
    yield client


@pytest.fixture
def fixtures_dir() -> pathlib.Path:
    return pathlib.Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_dir() -> pathlib.Path:
    """ Specifically to avoid using pytest's `tmpdir` which uses
        py.path rather than pathlib.
        """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield pathlib.Path(tmpdir)
