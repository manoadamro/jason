from typing import Any

import flask


class App(flask.Flask):
    def __init__(self, name: str, config: Any, testing: bool = False, **kwargs: Any):
        super(App, self).__init__(name, **kwargs)
        config.update(self.config)
        self.config = config
        self.testing = testing

    def assert_mixin(self, mixin, item, condition=""):
        if not isinstance(self.config, mixin):
            raise TypeError(
                f"could not initialise {item}. "
                f"config must sub-class {mixin.__name__} {condition}"
            )
