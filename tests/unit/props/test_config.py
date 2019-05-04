from unittest import mock

import pytest

from jason.props import BatchValidationError, Int, config


@pytest.fixture
def config_obj():
    class MyConfig(config.ConfigObject):
        MY_INT = Int(default=321)

    return MyConfig


def test_default_value(config_obj):
    my_config = config_obj.load()
    assert my_config.MY_INT == 321


def test_define_value(config_obj):
    my_config = config_obj.load(my_int=123)
    assert my_config.MY_INT == 123


def test_get_value_from_env(config_obj):
    with mock.patch("jason.props.config.os.environ", {"MY_INT": 456}):
        my_config = config_obj.load()
    assert my_config.MY_INT == 456


def test_error_from_kwarg(config_obj):
    with pytest.raises(BatchValidationError):
        config_obj.load(my_int="thingy")


def test_error_from_env(config_obj):
    with mock.patch("jason.props.config.os.environ", {"MY_INT": "thingy"}):
        with pytest.raises(BatchValidationError):
            config_obj.load()


def test_dict_methods(config_obj):
    obj = config_obj.load()
    obj.update(MY_INT=456)
    assert obj.MY_INT == 456


def test_indexer_get(config_obj):
    obj = config_obj.load()
    assert obj["MY_INT"] == 321


def test_indexer_set(config_obj):
    obj = config_obj.load()
    obj["MY_INT"] = 456
    assert obj.MY_INT == 456
