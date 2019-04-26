from unittest import mock

import pytest

from jason.service import Service


@pytest.fixture
def service():
    service = Service(
        name="test", config=mock.Mock(), sidekicks=(mock.Mock(), mock.Mock())
    )
    service.set_up = mock.Mock()
    service.main = mock.Mock()
    service.tear_down = mock.Mock()
    service.on_error = mock.Mock()
    service.on_close = mock.Mock()
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
