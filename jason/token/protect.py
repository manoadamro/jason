import functools
from typing import Any, Callable

import flask

from . import base, rules


class Protect(base.TokenHandlerBase):
    def __init__(self, *token_rules: base.TokenRule):
        self.rules = rules.AllOf(*token_rules)

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def call(*args: Any, **kwargs: Any) -> Any:
            token = flask.g[self.G_KEY]
            self.rules.validate(token)
            return func(*args, **kwargs)

        return call
