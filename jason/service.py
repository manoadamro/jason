import threading
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
        except Exception:
            self.on_error()
            raise
        else:
            self.tear_down()
        finally:
            self.on_close()

    def set_up(self):
        ...

    def main(self):
        raise NotImplementedError

    def on_error(self):
        ...

    def tear_down(self):
        ...

    def on_close(self):
        ...
