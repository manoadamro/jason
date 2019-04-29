from typing import Type

from celery import Celery
from flask import Flask
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from waitress import serve

from .config import Config, props

db = SQLAlchemy()
migrate = Migrate()
cache = FlaskRedis()
celery = Celery()


class ServiceConfig(Config):
    SERVE_HOST = props.String(default="localhost")
    SERVE_PORT = props.Int(default=5000)


class RedisConfigMixin:
    REDIS_HOST = props.String()
    REDIS_PORT = props.Int()
    REDIS_PASS = props.String()


class RabbitConfigMixin:
    RABBIT_HOST = props.String(default="localhost")
    RABBIT_PORT = props.Int(default=5672)
    RABBIT_USER = props.String(default="guest")
    RABBIT_PASS = props.String(default="guest")


class PostgresConfigMixin:
    DB_DRIVER = props.String(default="postgresql")
    DB_HOST = props.String()
    DB_PORT = props.String()
    DB_USER = props.String(nullable=True)
    DB_PASS = props.String(nullable=True)
    TEST_DB_URL = props.String(default="sqlite:///:memory:")


def create_app(
    config: ServiceConfig,
    testing: bool = False,
    use_db: bool = False,
    use_cache: bool = False,
    use_celery: bool = False,
    use_migrate: bool = False,
):

    # create flask app
    app = Flask(__name__)
    app.testing = testing
    app.config.update(config.__dict__)

    if use_migrate and not use_db:
        raise ValueError("parameter 'use_migrate' can not be True if 'use_db' is False")

    # init cache (if required)
    if use_cache:
        if not isinstance(config, RedisConfigMixin):
            raise TypeError(
                f"could not initialise cache. "
                f"config does not sub-class {RedisConfigMixin.__name__}"
            )
        cache.init_app(
            app=app,
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            password=config.REDIS_PASS,
        )

    # init database (if required)
    if use_db:
        if not isinstance(config, PostgresConfigMixin):
            raise TypeError(
                f"could not initialise database. "
                f"config does not sub-class {PostgresConfigMixin.__name__}"
            )
        if testing:
            database_uri = config.TEST_DB_URL
        else:
            if config.DB_USER:
                credentials = f"{config.DB_USER}:{config.DB_PASS}@"
            else:
                credentials = ""
            host = f"{config.DB_HOST}:{config.DB_PORT}"
            database_uri = f"{config.DB_DRIVER}://{credentials}{host}"
        app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app=app)

    # init celery (if required)
    if use_celery:
        if not isinstance(config, RabbitConfigMixin):
            raise TypeError(
                f"could not initialise celery. "
                f"config does not sub-class {RabbitConfigMixin.__name__}"
            )

        celery.conf.broker_url = ""  # TODO
        celery.conf.result_backend = ""  # TODO
        task_base = celery.Task

        class AppContextTask(task_base):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return task_base.__call__(self, *args, **kwargs)

        celery.Task = AppContextTask
        celery.finalize()

    # run database migrations (if required)
    if use_migrate:
        migrate.init_app(app=app, db=db)

    # we're done!
    return app


def flask_service(
    config_class: Type[ServiceConfig],
    use_db: bool = False,
    use_cache: bool = False,
    use_celery: bool = False,
):
    def wrapped(func):
        def call(debug=False, no_serve=False, **config_values):
            config = config_class.load(**config_values)

            app = create_app(
                config=config,
                testing=debug,
                use_db=use_db,
                use_cache=use_cache,
                use_celery=use_celery,
            )
            func(app, debug)

            if no_serve:
                return

            if debug:
                app.run(host=config.SERVE_HOST, port=config.SERVE_PORT)
            else:
                serve(app, host=config.SERVE_HOST, port=config.SERVE_PORT)

        return call

    return wrapped
