from typing import Any, Callable, Tuple, Type, Union

from .. import error, range
from .property import Property


class Number(Property):
    def __init__(
        self,
        min_value: Union[Callable[[], int], int] = None,
        max_value: Union[Callable[[], int], int] = None,
        allow_strings: bool = True,
        types: Tuple[Type, ...] = (int, float, str),
        **kwargs: Any,
    ):
        super(Number, self).__init__(types=types, **kwargs)
        self.range = range.RangeCheck(min_value=min_value, max_value=max_value)
        self.allow_strings = allow_strings

    def _from_string(self, value: str) -> Union[int, float]:
        if not self.allow_strings:
            raise error.PropertyValidationError(
                "Loading number from string is not allowed"
            )
        if "." in value and value.replace(".", "", 1).isnumeric():
            value = float(value)
        elif value.isnumeric():
            value = int(value)
        else:
            raise error.PropertyValidationError(
                f"Could not coerce string '{value}' to number"
            )
        return value

    def _validate(self, value: Union[int, float, str]) -> Union[int, float]:
        if isinstance(value, str):
            value = self._from_string(value)
        self.range.validate(value)
        return value


class Int(Number):
    def __init__(self, **kwargs: Any):
        super(Int, self).__init__(types=(str, int), **kwargs)

    def _validate(self, value: Union[int, str]) -> int:
        return super(Int, self)._validate(value)


class Float(Number):
    def __init__(self, **kwargs: Any):
        super(Float, self).__init__(types=(str, int, float), **kwargs)

    def _validate(self, value: Union[int, float, str]) -> float:
        value = super(Float, self)._validate(value)
        return float(value)
