from typing import Any, Dict, NoReturn

from jason import props

from .. import base


class HasKeys(base.TokenRule):
    def __init__(self, *keys: str):
        self.keys = keys

    def validate(self, token: Dict[str, Any]) -> NoReturn:
        errors = []
        for key in self.keys:
            if key not in token:
                errors.append(f"token is missing a required key {key}")
        if len(errors):
            raise props.BatchValidationError(
                f"token is missing one or more required keys", errors
            )
