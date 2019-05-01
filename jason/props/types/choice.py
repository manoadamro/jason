from typing import Any, List

from .. import error
from .property import Property


class Choice(Property):
    def __init__(
        self, choices: List = None, nullable: bool = False, default: Any = None
    ):
        super(Choice, self).__init__(nullable=nullable, default=default)
        self.choices = choices

    def _validate(self, value: Any) -> Any:
        if self.choices and value not in self.choices:
            raise error.PropertyValidationError(
                f"Property was expected to be one of: {', '.join((str(c) for c in self.choices))}"
            )
        return value
