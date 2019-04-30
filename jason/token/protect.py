import functools
from typing import Any, Callable

import flask

from . import base, rules


class Protect(base.TokenHandlerBase):
    """
    intended for use on flask endpoints
    ensures that the current token (stored in g) passes all of the defined rules

    >>> @token_protect(HasScopes("some:thing", "other:thing"), MatchValues("token:user_id", "url:user_id"))
    ... def some_route():
    ...     ...
    """

    def __init__(self, *token_rules: base.TokenRule):
        self.rules = rules.AllOf(*token_rules)

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def call(*args: Any, **kwargs: Any) -> Any:
            token = flask.g[self.G_KEY]
            self.rules.validate(token)
            return func(*args, **kwargs)

        return call


protect = Protect
