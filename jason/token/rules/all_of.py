from typing import Any, Dict, NoReturn

from jason import props

from .. import base, error


class AllOf(base.TokenRule):
    def __init__(self, *rules: base.TokenRule):
        self.rules = rules

    def validate(self, token: Dict[str, Any]) -> NoReturn:
        errors = []
        for rule in self.rules:
            try:
                rule.validate(token)
            except error.TokenValidationError as ex:
                errors.append(ex)
        if len(errors):
            raise props.BatchValidationError(
                "token did not conform to one or more of the defined rules", errors
            )
        return
