from jason import mixins
try:
    import celery
except ImportError:
    raise ImportError()  # TODO


class Celery(celery.Celery):

    def __init__(self):
        super(Celery, self).__init__()
        self.app = None

    def init_app(self, app):
        self.app = app
        app.assert_mixin(mixins.CeleryConfigMixin, "celery")

        self.conf.broker_url = self._celery_backend_url(
            app.config.CELERY_BROKER_BACKEND
        )
        self.conf.result_backend = self._celery_backend_url(
            app.config.CELERY_RESULTS_BACKEND
        )
        task_base = self.Task

        class AppContextTask(task_base):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return task_base.__call__(self, *args, **kwargs)

        # noinspection PyPropertyAccess
        self.Task = AppContextTask
        self.finalize()
        app.extensions["celery"] = celery

    def _redis_uri(self, database_id: int = None):
        if self.app.config.REDIS_PASS is not None:
            credentials = f":{self.app.config.REDIS_PASS}@"
        else:
            credentials = None
        uri = f"{self.app.config.REDIS_DRIVER}://{credentials}{self.app.config.REDIS_HOST}:{self.app.config.REDIS_PORT}"
        if database_id is not None:
            uri += f"/{database_id}"
        return uri

    def _rabbit_uri(self):
        return (
            f"{self.app.config.RABBIT_DRIVER}://"
            f"{self.app.config.RABBIT_USER}:{self.app.config.RABBIT_PORT}"
            f"@{self.app.config.RABBIT_HOST}:{self.app.config.RABBIT_PORT}"
        )

    def _check_backend_config(self, backend):
        if backend == "ampq":
            self.app.assert_mixin(
                mixins.RabbitConfigMixin,
                "celery broker",
                "if broker backend is rabbitmq",
            )
        elif backend == "redis":
            self.app.assert_mixin(
                mixins.RedisConfigMixin,
                "celery broker",
                "if broker backend is redis",
            )

    def _celery_backend_url(self, backend):
        self._check_backend_config(backend=backend)
        if backend == "ampq":
            return self._rabbit_uri()
        elif backend == "redis":
            return self._redis_uri(database_id=self.app.config.CELERY_REDIS_DATABASE_ID)
        raise ValueError(f"invalid backend name '{backend}'")
