from typing import Any

from jason.utils.encoder import JSONEncoder

from .patch import MonkeyFlask


class App(MonkeyFlask):
    json_encoder = JSONEncoder

    def __init__(
        self,
        name: str,
        config: Any,
        testing: bool = False,
        json_encoder=None,
        **kwargs: Any,
    ):
        super(App, self).__init__(name, **kwargs)
        config.update(self.config)
        self.config = config
        self.testing = testing
        self.json_encoder = json_encoder or self.json_encoder

    def assert_mixin(self, mixin, item, condition=""):
        if not isinstance(self.config, mixin):
            raise TypeError(
                f"could not initialise {item}. "
                f"config must sub-class {mixin.__name__} {condition}"
            )
