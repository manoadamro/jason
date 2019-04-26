import threading
from typing import Iterable, Type

from jason.config import Config, props

Config = Config
props = props


class Service:
    """
    Base class for all services.

    """

    def __init__(
        self, name: str, config: Type[Config], sidekicks: Iterable["Service"] = ()
    ):
        self.name = name
        self.config = config
        self.sidekicks = sidekicks

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
