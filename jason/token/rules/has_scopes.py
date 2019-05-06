from typing import Any, Dict, NoReturn

from jason import props

from .. import base


class HasScopes(base.TokenRule):
    def __init__(self, *scopes: str):
        self.scopes = scopes

    def validate(self, token: Dict[str, Any]) -> NoReturn:
        errors = []
        for scope in self.scopes:
            if scope not in token["scp"]:
                errors.append(f"token is missing a required scope {scope}")
        if len(errors):
            raise props.BatchValidationError(
                f"token is missing one or more required scopes", errors
            )
