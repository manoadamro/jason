from typing import Any, Union

from .. import error
from .property import Property


class Bool(Property):
    def __init__(self, allow_strings: bool = True, **kwargs: Any):
        super(Bool, self).__init__(types=(str, bool), **kwargs)
        self.allow_strings = allow_strings

    def _from_string(self, value: str) -> bool:

        if not self.allow_strings:
            raise error.PropertyValidationError(
                "Loading boolean from string is not allowed"
            )
        value = value.lower()
        if value == "true":
            value = True
        elif value == "false":
            value = False
        else:
            raise error.PropertyValidationError(
                f"Could not coerce string '{value}' to boolean"
            )
        return value

    def _validate(self, value: Union[str, bool]) -> bool:

        if isinstance(value, str):
            value = self._from_string(value)
        return value
