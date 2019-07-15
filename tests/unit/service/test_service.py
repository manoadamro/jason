from unittest import mock

import flask

from jason.service.service import Service, ServiceConfig, threading, waitress


def test_run_prod():
    service = Service(ServiceConfig)
    with mock.patch.object(waitress, "serve") as mock_serve, mock.patch.object(
        service, "_set_up"
    ):
        service.run(testing=False)
    assert mock_serve.call_count == 1


def test_run_testing():
    service = Service(ServiceConfig)
    service._app_gen = mock.MagicMock()
    with mock.patch.object(service, "_set_up"):
        service.run(testing=True)
    assert service._app.run.call_count == 1


def test_run_no_serve():
    service = Service(ServiceConfig)
    with mock.patch.object(waitress, "serve") as mock_serve, mock.patch.object(
        service, "_set_up"
    ):
        service.run(testing=False, no_serve=True)
    assert mock_serve.call_count == 0


def test_service_threads():
    service = Service(ServiceConfig)

    with mock.patch.object(service, "_set_up"), mock.patch.object(
        service, "_app_gen"
    ) as mock_gen:
        mock_threads = mock.Mock()
        mock_gen.return_value.extensions = {"service_threads": mock_threads}
        service.run(no_serve=True)
    assert mock_threads.run_all.call_count == 1


def test_run_detached():
    service = Service(ServiceConfig)
    with mock.patch.object(threading, "Thread") as mock_thread, mock.patch.object(
        service, "_set_up"
    ):
        service.run(detach=True)
    assert mock_thread.return_value.start.call_count == 1


def test_app():
    service = Service(ServiceConfig)
    with mock.patch.object(service, "_set_up"):
        app = service.app()
    assert isinstance(app, flask.Flask)
    assert app.testing is False


def test_test_app():
    service = Service(ServiceConfig)
    with mock.patch.object(service, "_set_up"):
        app = service.test_app()
    assert isinstance(app, flask.Flask)
    assert app.testing is True


def test_config():
    service = Service(ServiceConfig)
    with mock.patch.object(service, "_set_up"):
        config = service.config()
    assert isinstance(config, str)


def test_extensions():
    service = Service(ServiceConfig)
    with mock.patch.object(service, "_set_up"):
        ext = service.extensions()
    assert isinstance(ext, str)
