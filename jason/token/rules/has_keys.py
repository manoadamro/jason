from typing import Any, Dict, NoReturn

from .. import base, error


class HasKeys(base.TokenRule):
    def __init__(self, *keys: str):
        self.keys = keys

    def validate(self, token: Dict[str, Any]) -> NoReturn:

        if not all(key in token for key in self.keys):
            raise error.TokenValidationError(f"token is missing a required key")
