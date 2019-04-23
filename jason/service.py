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
    def __init__(
        self, config: Any, sidekicks: Iterable["Service"] = (), db_handler=None
    ):
        self.config = config
        self.sidekicks = sidekicks
        self.db_handler = db_handler

    def start(self):
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
        ...

    def main(self):
        ...

    def tear_down(self):
        ...

    def on_error(self, ex):
        ...

    def on_close(self):
        ...


class FlaskService(Service):
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
        app = flask.Flask(__name__)
        app.config.update(self.config.__dict__)
        app.config["DB_HANDLER"] = self.db_handler
        return app

    def serve(self):
        waitress.serve(
            self.app, host=self.config.SERVE_HOST, port=self.config.SERVE_PORT
        )


class RabbitService(Service):
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
        return PlainCredentials(
            username=self.config.RABBIT_USER, password=self.config.RABBIT_PASS
        )

    @property
    def connection_parameters(self, **kwargs):
        return ConnectionParameters(
            host=self.config.RABBIT_HOST,
            port=self.config.RABBIT_PORT,
            credentials=self.credentials,
            **kwargs
        )

    def create_connection(self):
        return BlockingConnection(self.connection_parameters)
