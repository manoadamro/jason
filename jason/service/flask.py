from typing import Iterable

from ..config.flask import FlaskConfigMixin
from .base import Service

try:
    import flask
    import waitress
except ImportError as ex:
    raise ImportError(
        f"to use this service module you will need both flask and waitress installed.\n"
        f"original error:"
        f"\n{ex}"
    )


class FlaskService(Service):
    """
    Base class for flask services

    """

    def __init__(self, config: FlaskConfigMixin, sidekicks: Iterable["Service"] = ()):
        super(FlaskService, self).__init__(config=config, sidekicks=sidekicks)
        self.app = self.create_app()
        self.app.config.update(self.config.__dict__)

    def create_app(self):
        """
        creates an instance of a flask app and returns

        """
        return flask.Flask(__name__)

    def main(self):
        """
        use waitress to serve

        """
        waitress.serve(
            self.app, host=self.config.SERVE_HOST, port=self.config.SERVE_PORT
        )
