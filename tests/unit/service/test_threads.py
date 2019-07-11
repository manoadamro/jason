from unittest import mock

import pytest

from jason.service.threads import ServiceThreads, threading


@pytest.fixture
def threads():
    mock_app = mock.MagicMock()
    threads = ServiceThreads()
    threads.init_app(mock_app)
    return threads


def test_add(threads):
    method = lambda x: None
    threads.add(method)
    assert {"method": method, "app": threads.app} in threads._service_threads


def test_run_all(threads):
    thread_count = 5
    with mock.patch.object(threading, "Thread") as mock_thread:
        for i in range(thread_count):
            threads.add(lambda _: i)
        threads.run_all()
    for thread in threads._service_threads:
        threads._run_with_context(thread)
    assert mock_thread.call_count == thread_count
