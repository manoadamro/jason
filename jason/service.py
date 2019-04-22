import threading
import flask
from typing import Iterable

from jason.core import configuration

Config = configuration.Config
props = configuration.props


class Service:
    def __init__(
        self, config: Config, sidekicks: Iterable["Service"] = (), db_handler=None
    ):
        self.config = config
        self.sidekicks = sidekicks
        self.db_handler = db_handler

    def start(self):
        self.set_up()
        for sidekick in self.sidekicks:
            if not sidekick:
                continue
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

    def __init__(self, *args, **kwargs):
        super(FlaskService, self).__init__(*args, **kwargs)
        self.app = self.create_app()

    def create_app(self):
        app = flask.Flask(__name__)
        app.config.update(self.config.__dict__)
        app.config["DB_HANDLER"] = self.db_handler
        return app
