from unittest import mock

import pytest

from jason.service import App, make_config


@pytest.fixture
def app():
    return App(__name__, make_config())


def test_init_token_handler(app):
    mock_obj = mock.Mock()
    app.init_token_handler(mock_obj)
    assert mock_obj.init_app.call_count == 1


def test_init_threads(app):
    mock_obj = mock.Mock()
    app.init_threads(mock_obj)
    assert mock_obj.init_app.call_count == 1


def test_init_sqlalchemy(app):
    app = App(__name__, make_config("postgres"))
    mock_obj1 = mock.Mock()
    mock_obj2 = mock.Mock()
    app.init_sqlalchemy(mock_obj1, mock_obj2)
    assert mock_obj1.init_app.call_count == 1
    assert mock_obj2.init_app.call_count == 1


def test_init_sqlalchemy_with_credentials(app):
    config = make_config("postgres").load()
    config.DB_USER = "user"
    config.DB_PASS = "password"
    app = App(__name__, config)
    mock_obj1 = mock.Mock()
    app.init_sqlalchemy(mock_obj1)
    assert mock_obj1.init_app.call_count == 1


def test_init_sqlalchemy_testing(app):
    config = make_config("postgres").load()
    app = App(__name__, config, testing=True)
    mock_obj1 = mock.Mock()
    app.init_sqlalchemy(mock_obj1)
    assert mock_obj1.init_app.call_count == 1


def test_init_sqlalchemy_fails(app):
    mock_obj = mock.Mock()
    with pytest.raises(TypeError):
        app.init_sqlalchemy(mock_obj)


def test_init_redis(app):
    app = App(__name__, make_config("redis"))
    mock_obj = mock.Mock()
    app.init_redis(mock_obj)
    assert mock_obj.init_app.call_count == 1


def test_init_redis_with_id(app):
    config = make_config("redis").load()
    config.REDIS_PASS = "password"
    app = App(__name__, config)
    mock_obj = mock.Mock()
    app.init_redis(mock_obj)
    assert mock_obj.init_app.call_count == 1


def test_init_redis_fails(app):
    mock_obj = mock.Mock()
    with pytest.raises(TypeError):
        app.init_redis(mock_obj)


def test_init_celery_rabbit():
    app = App(__name__, make_config("celery", "rabbit"))
    mock_obj = mock.Mock()
    app.init_celery(mock_obj)


def test_init_celery_redis():
    config = make_config("celery", "redis").load()
    config.CELERY_BROKER_BACKEND = "redis"
    config.CELERY_RESULTS_BACKEND = "redis"
    config.CELERY_REDIS_DATABASE_ID = "0"
    app = App(__name__, config)
    mock_obj = mock.Mock()
    app.init_celery(mock_obj)


def test_init_celery_fails(app):
    mock_obj = mock.Mock()
    with pytest.raises(TypeError):
        app.init_celery(mock_obj)


def test_init_celery_fails_with_invalid_backend(app):
    config = make_config("celery").load()
    config.CELERY_BROKER_BACKEND = "nope"
    config.CELERY_RESULTS_BACKEND = "nope"
    app = App(__name__, config)
    mock_obj = mock.Mock()
    with pytest.raises(ValueError):
        app.init_celery(mock_obj)
