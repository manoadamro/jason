import waitress

from jason.config import Config, props

Config = Config
props = props


class FlaskConfigMixin:
    SERVE_HOST = props.String(default="localhost")
    SERVE_PORT = props.Int(default=5000)


def serve(app, config, testing=False):
    if testing:
        app.run(host=config.SERVE_HOST, port=config.SERVE_PORT)
    else:
        waitress.serve(app, host=config.SERVE_HOST, port=config.SERVE_PORT)


def create_app():
    ...
