import functools
from typing import Any, Callable

import flask

from ..error import BatchValidationError
from ..exception import Unauthorized
from . import base, rules


class Protect(base.TokenHandlerBase):
    def __init__(self, *token_rules: base.TokenRule):
        self.rules = rules.AllOf(*token_rules)

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def call(*args: Any, **kwargs: Any) -> Any:
            token = flask.g[self.G_KEY]
            try:
                self.rules.validate(token)
            except BatchValidationError as ex:
                raise Unauthorized(ex.message)
            return func(*args, **kwargs)

        return call
