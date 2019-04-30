from typing import Any, Type

import flask
import waitress

from jason import props


class ServiceConfig(props.Config):
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
    _CELERY_BACKENDS = ["rabbitmq", "redis"]
    CELERY_BROKER_BACKEND = props.String(default="rabbitmq", choices=_CELERY_BACKENDS)
    CELERY_RESULTS_BACKEND = props.String(default="rabbitmq", choices=_CELERY_BACKENDS)
    CELERY_REDIS_DATABASE_ID = props.Int(default=0)


class WorkforceConfigMixin:
    ...


class FlaskApp(flask.Flask):
    def __init__(self, name: str, config: Any, testing: bool = False, **kwargs: Any):
        super(FlaskApp, self).__init__(name, **kwargs)
        self.testing = testing
        self.config = config

    def init_database(self, database, migrate=None):
        self._assert_mixin(self.config, PostgresConfigMixin, "database")
        database_uri = self._database_uri()
        self.config["SQLALCHEMY_DATABASE_URI"] = database_uri
        self.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        database.init_app(app=self)
        if migrate:
            migrate.init_app(app=self, db=database)

    def init_cache(self, cache):
        self._assert_mixin(self.config, RedisConfigMixin, "cache")
        cache.init_app(
            app=self,
            host=self.config.REDIS_HOST,
            port=self.config.REDIS_PORT,
            password=self.config.REDIS_PASS,
        )

    def init_celery(self, celery):
        self._assert_mixin(self.config, CeleryConfigMixin, "celery")

        def backend_url(backend):
            if backend == "rabbitmq":
                self._assert_mixin(
                    self.config,
                    RabbitConfigMixin,
                    "celery broker",
                    "if broker backend is rabbitmq",
                )
                return self._rabbit_uri()
            elif backend == "redis":
                self._assert_mixin(
                    self.config,
                    RedisConfigMixin,
                    "celery broker",
                    "if broker backend is redis",
                )
                return self._redis_uri(database_id=self.config.CELERY_REDIS_DATABASE_ID)
            raise ValueError(f"invalid backend name '{backend}'")

        celery.conf.broker_url = backend_url(self.config.CELERY_BROKER_BACKEND)
        celery.conf.result_backend = backend_url(self.config.CELERY_RESULTS_BACKEND)
        task_base = celery.Task

        class AppContextTask(task_base):
            abstract = True

            def __call__(self, *args, **kwargs):
                with self.app_context():
                    return task_base.__call__(self, *args, **kwargs)

        # noinspection PyPropertyAccess
        celery.Task = AppContextTask
        celery.finalize()

    def init_consumer(self, consumer):
        self._assert_mixin(self.config, WorkforceConfigMixin, "consumer")
        consumer.init_app(app=self)  # TODO kwargs from config (WorkforceConfigMixin

    @staticmethod
    def _assert_mixin(config, mixin, item, condition=""):
        if not isinstance(config, mixin):
            raise TypeError(
                f"could not initialise {item}. "
                f"config must sub-class {mixin.__name__} {condition}"
            )

    def _redis_uri(self, database_id: int = None):
        if self.config.REDIS_PASS is not None:
            credentials = f":{self.config.REDIS_PASS}@"
        else:
            credentials = None
        uri = f"{self.config.REDIS_DRIVER}://{credentials}{self.config.REDIS_HOST}:{self.config.REDIS_PORT}"
        if database_id is not None:
            uri += f"/{database_id}"
        return uri

    def _rabbit_uri(self):
        return (
            f"{self.config.RABBIT_DRIVER}://"
            f"{self.config.RABBIT_USER}:{self.config.RABBIT_PORT}"
            f"@{self.config.RABBIT_HOST}:{self.config.RABBIT_PORT}"
        )

    def _database_uri(self):
        if self.testing:
            return self.config.TEST_DB_URL
        if self.config.DB_USER:
            credentials = f"{self.config.DB_USER}:{self.config.DB_PASS}@"
        else:
            credentials = ""
        host = f"{self.config.DB_HOST}:{self.config.DB_PORT}"
        return f"{self.config.DB_DRIVER}://" f"{credentials}{host}"


class FlaskService:
    def __init__(self, config_class: Type[ServiceConfig], _app_gen: Any = FlaskApp):
        self._app_gen = _app_gen
        self.config_class = config_class
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
            self.app = self._app_gen.new(config=self.config, testing=self.debug)
            func(self.app, debug)
            if not no_serve:
                self._serve(host=self.config.SERVE_HOST, port=self.config.SERVE_PORT)

        return call


flask_service = FlaskService
