from typing import Any, Dict, NoReturn

from .. import base, error


class AnyOf(base.TokenRule):
    def __init__(self, *rules: base.TokenRule):
        self.rules = rules

    def validate(self, token: Dict[str, Any]) -> NoReturn:
        for rule in self.rules:
            try:
                rule.validate(token)
            except (error.TokenValidationError, error.BatchValidationError):
                continue
            else:
                return
        raise error.TokenValidationError(
            "token did not conform to any of the defined rules"
        )
