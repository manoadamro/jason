from unittest import mock

import pytest

from jason.service.rabbit import RabbitService


@pytest.fixture
def service():
    service = RabbitService(
        config=mock.Mock(
            RABBIT_HOST="localhost",
            RABBIT_PORT=12345,
            RABBIT_USER="guest",
            RABBIT_PASS="Pa$$w0rd",
        ),
        sidekicks=(mock.Mock(), mock.Mock()),
    )
    service.set_up = mock.Mock()
    service.main = mock.Mock()
    service.tear_down = mock.Mock()
    service.on_error = mock.Mock()
    service.on_close = mock.Mock()
    service.serve = mock.Mock()
    return service


def test_successful_run(service):
    service.start()
    assert service.set_up.call_count == 1
    assert service.main.call_count == 1
    assert service.tear_down.call_count == 1
    assert service.on_error.call_count == 0
    assert service.on_close.call_count == 1


def test_failed_run(service):
    service.main = mock.Mock(side_effect=Exception())
    with pytest.raises(Exception):
        service.start()
    assert service.set_up.call_count == 1
    assert service.main.call_count == 1
    assert service.tear_down.call_count == 0
    assert service.on_error.call_count == 1
    assert service.on_close.call_count == 1


def test_credentials(service):
    assert service.credentials.username == "guest"
    assert service.credentials.password == "Pa$$w0rd"


def test_connection_parameters(service):
    assert service.connection_parameters.host == "localhost"
    assert service.connection_parameters.port == 12345


def test_connection(service):
    with mock.patch("jason.service.rabbit.BlockingConnection") as mock_conn:
        service.create_connection()
    assert mock_conn.call_count == 1
