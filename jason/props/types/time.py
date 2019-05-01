import datetime
from typing import Any, Callable, Union

from .. import error, range
from .property import Property


class Date(Property):
    def __init__(
        self,
        min_value: Union[Callable[[], int], int] = None,
        max_value: Union[Callable[[], int], int] = None,
        allow_strings: bool = True,
        **kwargs: Any,
    ):
        super(Date, self).__init__(types=(datetime.date, str), **kwargs)
        self.range = range.RangeCheck(min_value=min_value, max_value=max_value)
        self.allow_strings = allow_strings

    def _from_string(self, value: str) -> datetime.date:

        if not self.allow_strings:
            raise error.PropertyValidationError(
                "Loading date from string is not allowed"
            )
        try:
            value = datetime.date.fromisoformat(value)
        except ValueError:
            raise error.PropertyValidationError(
                f"Could not coerce string '{value}' to date object"
            )
        return value

    def _validate(self, value: Union[str, datetime.date]) -> datetime.date:
        if isinstance(value, str):
            value = self._from_string(value)
        self.range.validate(value)
        return value


class Datetime(Property):
    def __init__(
        self,
        min_value: Union[Callable[[], int], int] = None,
        max_value: Union[Callable[[], int], int] = None,
        allow_strings: bool = True,
        **kwargs: Any,
    ):
        super(Datetime, self).__init__(types=(datetime.datetime, str), **kwargs)
        self.range = range.DateTimeRangeCheck(min_value=min_value, max_value=max_value)
        self.allow_strings = allow_strings

    def _from_string(self, value: str) -> datetime.datetime:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        if not self.allow_strings:
            raise error.PropertyValidationError(
                "Loading datetime from string is not allowed"
            )
        try:
            value = datetime.datetime.fromisoformat(value)
        except ValueError:
            raise error.PropertyValidationError(
                f"Could not coerce string '{value}' to datetime object"
            )
        return value

    def _validate(self, value: Union[datetime.datetime, str]) -> datetime.datetime:
        if isinstance(value, str):
            value = self._from_string(value)
        if value.tzinfo is None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        self.range.validate(value)
        return value
