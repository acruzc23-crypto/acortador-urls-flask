import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    return create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db"), "BASE_URL": "http://corto.test"})


@pytest.fixture
def client(app):
    return app.test_client()
