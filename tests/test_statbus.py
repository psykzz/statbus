import tempfile
import pytest
from statbus import create_app


@pytest.fixture
def client():
    db_fd, db_name = tempfile.mkstemp()
    config = {}
    config["DATABASE"] = {"name": db_name, "engine": "peewee.SqliteDatabase"}
    config["TESTING"] = True

    app = create_app(config)
    client = app.test_client()

    yield client

    # Cleanup
    os.close(db_fd)
    os.unlink(db_name)


def test_assert(self):
    assert True


def test_homepage(client):
    """Start with a blank database."""

    rv = client.get("/")
    assert b"Welcome!" in rv.data
