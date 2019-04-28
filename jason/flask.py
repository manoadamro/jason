import flask
import waitress
from .config import Config, props
from .cache import RedisCache, RedisConfigMixin
from .database import Database, PostgresConfigMixin
from .schema import request_schema

Config = Config
PostgresConfigMixin = PostgresConfigMixin
RedisConfigMixin = RedisConfigMixin

props = props
request_schema = request_schema

db = Database()
cache = RedisCache()


class FlaskConfigMixin:
    SERVE_HOST = props.String(default="localhost")
    SERVE_PORT = props.Int(default=5000)


def serve_app(app, config, testing=False):
    if testing:
        app.run(host=config.SERVE_HOST, port=config.SERVE_PORT)
    else:
        waitress.serve(app, host=config.SERVE_HOST, port=config.SERVE_PORT)


def create_app(config, testing=False, use_db=False, use_cache=False):
    app = flask.Flask(__name__)
    app.testing = testing
    app.config.update(config.__dict__)
    if use_db:
        db.init(config=config, testing=testing)
        app.config["DB"] = db
    if use_cache:
        cache.init(config=config, testing=testing)
        app.config["CACHE"] = cache
    return app


def flask_service(config_class, use_db=False, use_cache=False):

    def wrapped(func):
        def call(debug=False, no_serve=False, **kwargs):
            config = config_class.load(**kwargs)

            app = create_app(
                config=config, testing=debug, use_db=use_db, use_cache=use_cache
            )
            func(app, debug)

            if not no_serve:
                serve_app(app=app, config=config, testing=debug)

        return call

    return wrapped
