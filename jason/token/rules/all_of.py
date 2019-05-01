from typing import Any, Dict, NoReturn

from .. import base, error


class AllOf(base.TokenRule):
    def __init__(self, *rules: base.TokenRule):
        self.rules = rules

    def validate(self, token: Dict[str, Any]) -> NoReturn:
        for rule in self.rules:
            try:
                rule.validate(token)
            except error.TokenValidationError as ex:
                raise error.TokenValidationError(
                    f"token did not conform to one or more of the defined rules. {ex}"
                )
        return
