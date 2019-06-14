import pytest

from jason.props.config import ConfigObject
from jason.service import App
from jason.service.mixins import PostgresConfigMixin, RedisConfigMixin


@pytest.fixture
def config_obj():
    class Config(ConfigObject, PostgresConfigMixin):
        ...

    return Config


def test_assert_mixin(config_obj):
    app = App("my_app", config=config_obj.load())
    app.assert_mixin(PostgresConfigMixin, "test")


def test_assert_mixin_fails(config_obj):
    app = App("my_app", config=config_obj.load())
    with pytest.raises(TypeError):
        app.assert_mixin(RedisConfigMixin, "test")
