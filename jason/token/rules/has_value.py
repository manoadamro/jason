from typing import Any, Dict, NoReturn

import jsonpointer

from jason.props.base import SchemaAttribute, SchemaRule

from .. import base, error


class HasValue(base.TokenRule):
    def __init__(self, pointer: str, value: Any):
        if not pointer.startswith("/"):
            pointer = f"/{pointer}"
        self.pointer = pointer
        self.value = value

    def validate(self, token: Dict[str, Any]) -> NoReturn:
        try:
            v = jsonpointer.resolve_pointer(token, self.pointer)
            if isinstance(self.value, (SchemaAttribute, SchemaRule)):
                self.value.load(v)
            elif v != self.value:
                raise error.TokenValidationError(
                    f"token value at defined path does not match defined value"
                )
        except jsonpointer.JsonPointerException:
            raise error.TokenValidationError(f"token is missing a required value")
