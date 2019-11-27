import tempfile
import pytest
from statbus import create_app


@pytest.fixture
def client():
    self.db_fd, self.db_name = tempfile.mkstemp()
    config = {}
    config["DATABASE"] = {"name": self.db_name, "engine": "peewee.SqliteDatabase"}
    config["TESTING"] = True

    app = create_app(config)
    client = app.test_client()

    yield client

    # Cleanup
    os.close(self.db_fd)
    os.unlink(self.db_name)


def test_assert(self):
    assert True


def test_homepage(client):
    """Start with a blank database."""

    rv = client.get("/")
    assert b"Welcome!" in rv.data
