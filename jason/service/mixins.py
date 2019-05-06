from jason import props


class RedisConfigMixin:
    REDIS_DRIVER = props.String(default="redis")
    REDIS_HOST = props.String(default="localhost")
    REDIS_PORT = props.Int(default=6379)
    REDIS_PASS = props.String(nullable=True)


class RabbitConfigMixin:
    RABBIT_DRIVER = props.String(default="ampq")
    RABBIT_HOST = props.String(default="localhost")
    RABBIT_PORT = props.Int(default=5672)
    RABBIT_USER = props.String(default="guest")
    RABBIT_PASS = props.String(default="guest")


class PostgresConfigMixin:
    TEST_DB_URL = props.String(default="sqlite:///:memory:")
    DB_DRIVER = props.String(default="postgres")
    DB_HOST = props.String(default="localhost")
    DB_PORT = props.Int(default=5432)
    DB_USER = props.String(default="postgres")
    DB_PASS = props.String(default="postgres")
    DB_NAME = props.String(default="postgres")


class CeleryConfigMixin:
    _CELERY_BACKENDS = ["ampq", "redis"]
    CELERY_BROKER_BACKEND = props.Choice(default="ampq", choices=_CELERY_BACKENDS)
    CELERY_RESULTS_BACKEND = props.Choice(default="ampq", choices=_CELERY_BACKENDS)
    CELERY_REDIS_DATABASE_ID = props.String(default="0")
