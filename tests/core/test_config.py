from unittest.mock import patch

import pytest

from jason.core.configuration import Config, props


@pytest.fixture
def model():
    class MyConfig(Config):
        MY_INT = props.Int()
        MY_FLOAT = props.Float()
        MY_STRING = props.String()
        MY_BOOL = props.Bool()

    return MyConfig


@pytest.fixture
def environ():
    return {
        "MY_INT": "123",
        "MY_FLOAT": "12.3",
        "MY_STRING": "stringy",
        "MY_BOOL": "true",
    }


def test_loads_config_from_environment(environ, model):
    with patch("os.environ", environ):
        config = model.load()
    assert config.MY_INT == 123
    assert config.MY_FLOAT == 12.3
    assert config.MY_STRING == "stringy"
    assert config.MY_BOOL is True


def test_loads_config_from_kwargs(environ, model):
    kwargs = {key.lower(): value for key, value in environ.items()}
    with patch("os.environ", {}):
        config = model.load(**kwargs)
    assert config.MY_INT == 123
    assert config.MY_FLOAT == 12.3
    assert config.MY_STRING == "stringy"
    assert config.MY_BOOL is True


def test_kwargs_override_environment(environ, model):
    with patch("os.environ", environ):
        config = model.load(my_float=32.1, my_bool=False)
    assert config.MY_INT == 123
    assert config.MY_FLOAT == 32.1
    assert config.MY_STRING == "stringy"
    assert config.MY_BOOL is False


def test_bool_is_converted(model, environ):
    with patch("os.environ", environ):
        config = model.load()
    assert isinstance(config.MY_BOOL, bool)


def test_int_is_converted(model, environ):
    with patch("os.environ", environ):
        config = model.load()
    assert isinstance(config.MY_INT, int)


def test_float_is_converted(model, environ):
    with patch("os.environ", environ):
        config = model.load()
    assert isinstance(config.MY_FLOAT, float)
