import pytest

from jason import ServiceConfig, make_config, props


def get_fields(obj):
    return [name for name in dir(obj) if name.isupper() and not name.startswith("_")]


def test_redis():
    config = make_config("redis")
    assert hasattr(config, "REDIS_DRIVER")
    assert hasattr(config, "REDIS_HOST")
    assert hasattr(config, "REDIS_PORT")
    assert hasattr(config, "REDIS_PASS")


def test_rabbit():
    config = make_config("rabbit")
    assert hasattr(config, "RABBIT_DRIVER")
    assert hasattr(config, "RABBIT_HOST")
    assert hasattr(config, "RABBIT_PORT")
    assert hasattr(config, "RABBIT_USER")
    assert hasattr(config, "RABBIT_PASS")


def test_postgres():
    config = make_config("postgres")
    assert hasattr(config, "TEST_DB_URL")
    assert hasattr(config, "DB_DRIVER")
    assert hasattr(config, "DB_HOST")
    assert hasattr(config, "DB_PORT")
    assert hasattr(config, "DB_USER")
    assert hasattr(config, "DB_PASS")


def test_celery():
    config = make_config("celery")
    assert hasattr(config, "CELERY_BROKER_BACKEND")
    assert hasattr(config, "CELERY_RESULTS_BACKEND")
    assert hasattr(config, "CELERY_REDIS_DATABASE_ID")


def test_base():
    class MyConfig(ServiceConfig):
        SOME_THING = props.Int()

    config = make_config(MyConfig)
    assert hasattr(config, "SOME_THING")
    assert hasattr(config, "SERVE")
    assert hasattr(config, "SERVE_HOST")
    assert hasattr(config, "SERVE_PORT")


def test_default_base():
    config = make_config()
    assert hasattr(config, "SERVE")
    assert hasattr(config, "SERVE_HOST")
    assert hasattr(config, "SERVE_PORT")


def test_invalid():
    with pytest.raises(KeyError):
        make_config("nope")


def test_fields():
    config = make_config(thing=props.Int(), other=props.String())
    assert hasattr(config, "THING")
    assert hasattr(config, "OTHER")


def test_duplicate_mixin_names():
    with pytest.raises(ValueError):
        make_config("postgres", "postgres")


def test_two_base_classes():
    with pytest.raises(ValueError):
        make_config(type("A", (ServiceConfig,), {}), type("B", (ServiceConfig,), {}))


def test_some_class():
    a = type("A", (ServiceConfig,), {"a": 1})
    b = type("B", (), {"a": 1})
    assert issubclass(make_config(a, b), ServiceConfig)


def test_wrong_type():
    with pytest.raises(ValueError):
        make_config("postgres", 123)
