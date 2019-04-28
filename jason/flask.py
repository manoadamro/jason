import flask
import waitress

from jason.config import Config, props

from .cache import RedisCache
from .database import Database
from .utils import is_instance_or_type, is_type

Config = Config
props = props


db = Database()
cache = RedisCache()


class FlaskConfigMixin:
    SERVE_HOST = props.String(default="localhost")
    SERVE_PORT = props.Int(default=5000)


def serve(app, config, testing=False):
    if testing:
        app.run(host=config.SERVE_HOST, port=config.SERVE_PORT)
    else:
        waitress.serve(app, host=config.SERVE_HOST, port=config.SERVE_PORT)


def create_app(config, testing=False, use_db=False, use_cache=False):
    app = flask.Flask(__name__)
    testing.testing = testing
    if not is_instance_or_type(config, Config):
        raise TypeError(
            f"config object must be an instance or subclass of {Config.__name__}"
        )
    if is_type(config, Config):
        config = config.load()
    app.config.update(config.__dict__)
    if use_db:
        db.init(config=config, testing=testing)
        app.config["DB"] = db
    if use_cache:
        cache.init(config=config, testing=testing)
        app.config["CACHE"] = cache
    return app
