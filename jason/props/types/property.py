from typing import Any, Callable, List, Tuple, Type, Union

from .. import base, error, utils


class Property(base.SchemaAttribute):
    def __init__(
        self,
        nullable: bool = False,
        default: Any = None,
        types: Union[Tuple[Type, ...], List[Type]] = None,
    ):
        self.nullable = nullable
        self.default = default
        self.types = types

    def load(self, value: Any) -> Any:
        if value is None:
            value = utils.maybe_call(value=self.default)
        if value is None:
            if not self.nullable:
                raise error.PropertyValidationError(f"Property is not nullable")
            return None
        if self.types and (
            (utils.is_bool(value) and bool not in self.types)
            or not isinstance(value, self.types)
        ):
            raise error.PropertyValidationError(
                f"Property was expected to be of type: "
                f"{', '.join(t.__name__ for t in self.types)}. not {type(value).__name__}"
            )
        return self._validate(value)

    def _validate(self, value: Any) -> Any:
        return value

    def __call__(self, func: Callable[[Any], Any]) -> "Property":
        base_validator = self._validate

        def wrapped_validator(value: Any) -> Any:
            value = base_validator(value)
            return func(value)

        self._validate = wrapped_validator
        return self

    def is_identical_to(self, other):
        if not isinstance(other, type(self)):
            return False
        return utils.deep_compare(self, other)
