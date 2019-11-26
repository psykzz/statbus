import pytest

from statbus import create_app


@pytest.fixture
def client():
    config = {}
    config["DATABASE"] = {"name": "./testing.db", "engine": "peewee.SqliteDatabase"}
    config["TESTING"] = True

    app = create_app(config)
    client = app.test_client()

    yield client

    # Cleanup if required


def test_homepage(client):
    """Start with a blank database."""

    rv = client.get("/")
    assert b"Welcome!" in rv.data
