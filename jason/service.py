import threading
from typing import Any, Iterable

import flask
import waitress
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from .config.flask import FlaskConfigMixin
from .core.configuration import Config, props

Config = Config
props = props


class Service:
    """
    Base class for all services.

    """

    def __init__(
        self, config: Any, sidekicks: Iterable["Service"] = (), db_handler=None
    ):
        self.config = config
        self.sidekicks = sidekicks
        self.db_handler = db_handler

    def start(self):
        """
        starts and runs the service.

        """
        self.set_up()
        for sidekick in self.sidekicks:
            thread = threading.Thread(target=sidekick.start)
            thread.start()
        try:
            self.main()
        except Exception as ex:
            self.on_error(ex)
            raise
        else:
            self.tear_down()
        finally:
            self.on_close()

    def set_up(self):
        """
        called before `main` method

        """
        ...

    def main(self):
        """
        the main service method

        """
        ...

    def tear_down(self):
        """
        called when main method exits,
        assuming there were no errors

        """
        ...

    def on_error(self, ex):
        """
        called when main method exits due to an error

        """
        ...

    def on_close(self):
        """
        called before process exits,
        regardless of errors

        """
        ...


class FlaskService(Service):
    """
    Base class for flask services

    """

    def __init__(
        self,
        config: FlaskConfigMixin,
        sidekicks: Iterable["Service"] = (),
        db_handler: Any = None,
    ):
        super(FlaskService, self).__init__(
            config=config, sidekicks=sidekicks, db_handler=db_handler
        )
        self.app = self.create_app()

    def create_app(self):
        """
        creates an instance of a flask app and returns

        """
        app = flask.Flask(__name__)
        app.config.update(self.config.__dict__)
        app.config["DB_HANDLER"] = self.db_handler
        return app

    def serve(self):
        """
        use waitress to serve

        """
        waitress.serve(
            self.app, host=self.config.SERVE_HOST, port=self.config.SERVE_PORT
        )


class RabbitService(Service):
    """
    Base class for rabbit consumer services

    """

    def __init__(
        self,
        config: FlaskConfigMixin,
        sidekicks: Iterable["Service"] = (),
        db_handler: Any = None,
    ):
        super(RabbitService, self).__init__(
            config=config, sidekicks=sidekicks, db_handler=db_handler
        )
        self.connection = None
        self.channel = None

    @property
    def credentials(self):
        """
        rabbitmq connection credentials

        """
        return PlainCredentials(
            username=self.config.RABBIT_USER, password=self.config.RABBIT_PASS
        )

    @property
    def connection_parameters(self, **kwargs):
        """
        rabbitmq connection parameters

        """
        return ConnectionParameters(
            host=self.config.RABBIT_HOST,
            port=self.config.RABBIT_PORT,
            credentials=self.credentials,
            **kwargs
        )

    def create_connection(self):
        """
        creates a rabbitmq blocking connection

        """
        return BlockingConnection(self.connection_parameters)
