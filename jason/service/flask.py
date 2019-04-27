from typing import Iterable, Type

import flask
import waitress

from .base import Config as _Config
from .base import Service, props


class FlaskConfigMixin:
    SERVE_HOST = props.String(default="localhost")
    SERVE_PORT = props.Int(default=5000)


class Config(FlaskConfigMixin, _Config):
    ...


class FlaskService(Service):
    """
    Base class for flask services

    """

    def __init__(
        self,
        name: str,
        config: Type[Config],
        sidekicks: Iterable["Service"] = (),
        testing: bool = False,
        **kwargs
    ):
        super(FlaskService, self).__init__(
            name=name, config=config, sidekicks=sidekicks, testing=testing, **kwargs
        )
        self.app = self.create_app()
        self.app.config.update(self.config.__dict__)

    def create_app(self):
        """
        creates an instance of a flask app and returns

        """
        self.logger.info("creating flask app for service %s", self.name)
        return flask.Flask(self.name)

    def main(self):
        """
        use waitress to serve

        """
        self.logger.info("serving flask app %s with waitress", self.name)
        waitress.serve(
            self.app, host=self.config.SERVE_HOST, port=self.config.SERVE_PORT
        )
