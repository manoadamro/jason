from typing import Any

import flask

from jason import props

from . import mixins
from ..props.utils import is_type


class App(flask.Flask):
    def __init__(self, name: str, config: Any, testing: bool = False, **kwargs: Any):
        super(App, self).__init__(name, **kwargs)
        if is_type(config, props.ConfigObject):
            config = config.load()
        config.update(self.config)
        self.config = config
        self.testing = testing

    def init_token_handler(self, handler):
        handler.init_app(self)

    def init_threads(self, app_threads):
        app_threads.init_app(app=self, config=self.config)

    def init_sqlalchemy(self, database, migrate=None):
        self._assert_mixin(self.config, mixins.PostgresConfigMixin, "database")
        self.config["SQLALCHEMY_DATABASE_URI"] = self._database_uri()
        self.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        database.init_app(app=self)
        if migrate is not None:
            migrate.init_app(app=self, db=database)
        if self.testing:
            with self.app_context():
                database.create_all()

    def init_redis(self, cache):
        self._assert_mixin(self.config, mixins.RedisConfigMixin, "cache")
        self.config.REDIS_URL = self._redis_uri()
        cache.init_app(app=self)

    def init_celery(self, celery):
        self._assert_mixin(self.config, mixins.CeleryConfigMixin, "celery")

        celery.conf.broker_url = self._celery_backend_url(
            self.config.CELERY_BROKER_BACKEND
        )
        celery.conf.result_backend = self._celery_backend_url(
            self.config.CELERY_RESULTS_BACKEND
        )
        task_base = celery.Task

        class AppContextTask(task_base):
            abstract = True

            def __call__(self, *args, **kwargs):
                with self.app_context():
                    return task_base.__call__(self, *args, **kwargs)

        # noinspection PyPropertyAccess
        celery.Task = AppContextTask
        celery.finalize()
        self.extensions["celery"] = celery

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
        return f"{self.config.DB_DRIVER}://{credentials}{self.config.DB_HOST}:{self.config.DB_PORT}"

    def _check_backend_config(self, backend):
        if backend == "ampq":
            self._assert_mixin(
                self.config,
                mixins.RabbitConfigMixin,
                "celery broker",
                "if broker backend is rabbitmq",
            )
        elif backend == "redis":
            self._assert_mixin(
                self.config,
                mixins.RedisConfigMixin,
                "celery broker",
                "if broker backend is redis",
            )

    def _celery_backend_url(self, backend):
        self._check_backend_config(backend=backend)
        if backend == "ampq":
            return self._rabbit_uri()
        elif backend == "redis":
            return self._redis_uri(database_id=self.config.CELERY_REDIS_DATABASE_ID)
        raise ValueError(f"invalid backend name '{backend}'")
