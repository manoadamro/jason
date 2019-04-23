from unittest import mock

import pytest

from jason.database import postgres_engine


@pytest.fixture
def config():
    return mock.Mock(
        DB_HOST="localhost",
        DB_PORT=9001,
        DB_USER="someone",
        DB_PASS="Pa$$w0rd",
        DB_DRIVER="postgres",
        TEST_DB_URL="sqlite:///:memory:",
    )


def test_testing_mode(config):
    with mock.patch("jason.database.db") as mock_db:
        postgres_engine(config=config, testing=True)
    mock_db.create_engine.assert_called_once_with("sqlite:///:memory:", echo=True)


def test_prod_mode(config):
    with mock.patch("jason.database.db") as mock_db:
        postgres_engine(config=config, testing=False)
    mock_db.create_engine.assert_called_once_with(
        "postgres://someone:Pa$$w0rd@localhost:9001", echo=True
    )


def test_prod_mode_no_login(config):
    config.DB_USER = None
    config.DB_PASS = None
    with mock.patch("jason.database.db") as mock_db:
        postgres_engine(config=config, testing=False)
    mock_db.create_engine.assert_called_once_with(
        "postgres://localhost:9001", echo=True
    )
