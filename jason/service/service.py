import threading
from typing import Any, Type

import waitress

from .app import App
from .config import ServiceConfig


class Service:
    def __init__(self, config_class: Type[ServiceConfig], _app_gen: Any = App):
        self._app_gen = _app_gen
        self._config_class = config_class
        self._app = None
        self._config = None
        self._callback = None

    def _serve(self, host, port):
        if self._config.TESTING:
            self._app.run(host=host, port=port)
        else:
            waitress.serve(self._app, host=host, port=port)

    def _pre_command(self, testing=None, config_values=None):
        if config_values is None:
            config_values = {}
        if testing is not None:
            config_values["TESTING"] = testing
        self._config = self._config_class.load(**config_values)
        self._app = self._app_gen(
            __name__, config=self._config, testing=self._config.TESTING
        )
        self._set_up(self._app)

    def _set_up(self, app):
        raise NotImplementedError

    @property
    def _autoapp(self):
        if self._app is None:
            self._pre_command()
        return self._app

    @property
    def app_context(self):
        return self._autoapp.app_context

    def run(self, testing=None, no_serve=False, detach=False, **config_values):
        self._pre_command(testing, config_values)
        if "service_threads" in self._app.extensions:
            service_threads = self._app.extensions["service_threads"]
            service_threads.run_all(threaded=False)
        if no_serve is False and self._config.SERVE is True:
            if not detach:
                self._serve(host=self._config.SERVE_HOST, port=self._config.SERVE_PORT)
            else:
                thread = threading.Thread(
                    target=self._serve,
                    kwargs={
                        "host": self._config.SERVE_HOST,
                        "port": self._config.SERVE_PORT,
                    },
                    daemon=True,
                )
                thread.start()
        else:
            while threading.active_count() - 1:
                ...

    def test_app(self, **config_values):
        self.run(testing=True, no_serve=True, **config_values)
        return self._app

    def app(self, testing=None, **config_values):
        self.run(testing=testing, no_serve=True, **config_values)
        return self._app

    def config(self, testing=None, **config_values):
        self._pre_command(testing, config_values)
        prop_strings = (
            f"{key}={value}" for key, value in self._config.__dict__.items()
        )
        return "\n".join(prop_strings)

    def extensions(self, testing=None, **config_values):
        self._pre_command(testing, config_values)
        return "\n".join(e for e in self._app.extensions)

    def __call__(self, func):
        self._set_up = func
        return self
