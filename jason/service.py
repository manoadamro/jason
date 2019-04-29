from typing import Any, Type

import celery
import flask
import flask_migrate
import flask_redis
import flask_sqlalchemy
import waitress

from .config import Config, props

db = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate()
cache = flask_redis.FlaskRedis()
celery = celery.Celery()


class ServiceConfig(Config):
    SERVE_HOST = props.String(default="localhost")
    SERVE_PORT = props.Int(default=5000)


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
    DB_DRIVER = props.String(default="postgresql")
    DB_HOST = props.String(default="localhost")
    DB_PORT = props.String(default=5432)
    DB_USER = props.String(nullable=True)
    DB_PASS = props.String(nullable=True)


class CeleryConfigMixin:
    CELERY_BROKER_BACKEND = props.String(
        default="rabbitmq", choices=["rabbitmq", "redis"]
    )
    CELERY_RESULTS_BACKEND = props.String(
        default="rabbitmq", choices=["rabbitmq", "redis"]
    )
    CELERY_REDIS_DATABASE_ID = props.Int(default=0)


def _assert_mixin(config, mixin, item, condition=""):
    if not isinstance(config, mixin):
        raise TypeError(
            f"could not initialise {item}. "
            f"config must sub-class {mixin.__name__} {condition}"
        )


def _redis_uri(config: RedisConfigMixin, database_id: int = None):
    if config.REDIS_PASS is not None:
        credentials = f":{config.REDIS_PASS}@"
    else:
        credentials = None
    uri = (
        f"{config.REDIS_DRIVER}://{credentials}{config.REDIS_HOST}:{config.REDIS_PORT}"
    )
    if database_id is not None:
        uri += f"/{database_id}"
    return uri


def _rabbit_uri(config: RabbitConfigMixin):
    return (
        f"{config.RABBIT_DRIVER}://"
        f"{config.RABBIT_USER}:{config.RABBIT_PORT}"
        f"@{config.RABBIT_HOST}:{config.RABBIT_PORT}"
    )


def _database_uri(config: PostgresConfigMixin, testing: bool):
    if testing:
        return config.TEST_DB_URL
    if config.DB_USER:
        credentials = f"{config.DB_USER}:{config.DB_PASS}@"
    else:
        credentials = ""
    host = f"{config.DB_HOST}:{config.DB_PORT}"
    return f"{config.DB_DRIVER}://" f"{credentials}{host}"


def _init_database(app, config, testing):
    _assert_mixin(config, PostgresConfigMixin, "database")
    database_uri = _database_uri(config, testing=testing)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app=app)


def _init_cache(app, config):
    _assert_mixin(config, RedisConfigMixin, "cache")
    cache.init_app(
        app=app,
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        password=config.REDIS_PASS,
    )


def _init_celery(app, config):
    _assert_mixin(config, CeleryConfigMixin, "celery")

    def backend_url(backend):
        if backend == "rabbitmq":
            _assert_mixin(
                config,
                RabbitConfigMixin,
                "celery broker",
                "if broker backend is rabbitmq",
            )
            return _rabbit_uri(config)
        elif backend == "redis":
            _assert_mixin(
                config, RedisConfigMixin, "celery broker", "if broker backend is redis"
            )
            return _redis_uri(
                config=config, database_id=config.CELERY_REDIS_DATABASE_ID
            )
        raise ValueError(f"invalid backend name '{backend}'")

    celery.conf.broker_url = backend_url(config.CELERY_BROKER_BACKEND)
    celery.conf.result_backend = backend_url(config.CELERY_RESULTS_BACKEND)
    task_base = celery.Task

    class AppContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)

    # noinspection PyPropertyAccess
    celery.Task = AppContextTask
    celery.finalize()


class _FlaskApp(flask.Flask):
    @classmethod
    def new(
        cls,
        config: Any,
        testing: bool = False,
        use_db: bool = False,
        use_cache: bool = False,
        use_celery: bool = False,
        use_migrate: bool = False,
    ):
        app = cls(__name__)
        app.testing = testing
        app.config.update(config.__dict__)
        if use_migrate and not use_db:
            raise ValueError(
                "parameter 'use_migrate' can not be True if 'use_db' is False"
            )
        if use_cache:
            _init_cache(app=app, config=config)
        if use_db:
            _init_database(app=app, config=config, testing=testing)
        if use_celery:
            _init_celery(app=app, config=config)
        if use_migrate:
            migrate.init_app(app=app, db=db)
        return app

    def register_consumer(self, channel):
        ...  # TODO start consumer on thread


class FlaskService:
    def __init__(
        self,
        config_class: Type[ServiceConfig],
        use_db: bool = False,
        use_cache: bool = False,
        use_celery: bool = False,
        _app_gen: Any = _FlaskApp
    ):
        self._app_gen = _app_gen
        self.config_class = config_class
        self.use_db = use_db
        self.use_cache = use_cache
        self.use_celery = use_celery
        self.app = None
        self.config = None
        self.debug = False

    def _serve(self, host, port):
        if self.debug:
            self.app.run(host=host, port=port)
        else:
            waitress.serve(self.app, host=host, port=port)

    def __call__(self, func):
        def call(debug=False, no_serve=False, **config_values):
            self.debug = debug
            self.config = self.config_class.load(**config_values)
            self.app = self._app_gen.new(
                config=self.config,
                testing=self.debug,
                use_db=self.use_db,
                use_cache=self.use_cache,
                use_celery=self.use_celery,
            )
            func(self.app, debug)
            if no_serve:
                return
            self._serve(host=self.config.SERVE_HOST, port=self.config.SERVE_PORT)

        return call


flask_service = FlaskService
