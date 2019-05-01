from typing import Any, Dict, NoReturn

from .. import base, error


class HasScopes(base.TokenRule):
    def __init__(self, *scopes: str):
        self.scopes = scopes

    def validate(self, token: Dict[str, Any]) -> NoReturn:
        if not all(scope in token["scp"] for scope in self.scopes):
            raise error.TokenValidationError(f"token is missing a required scope")
