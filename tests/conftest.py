import flask
import pytest

from appetiser import appetiser


@pytest.fixture
def appetiser_client() -> flask.Flask:
    appetiser.config['TESTING'] = True
    client = appetiser.test_client()
    yield client
