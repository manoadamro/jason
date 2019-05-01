import datetime
from typing import Any, Union

from . import error, utils


class RangeCheck:
    """
    ensures that a value is within a defined range.

    >>> check = RangeCheck(min_value=5, max_value=10)
    >>> check.validate(7)

    >>> check.validate(15)
    Traceback (most recent call last):
        ...
     jason.props.error.PropertyValidationError: Range validation failed. value is '15'. minimum: 5 maximum: 10

    >>> check.validate(3)
    Traceback (most recent call last):
        ...
     jason.props.error.PropertyValidationError: Range validation failed. value is '3'. minimum: 5 maximum: 10

    """

    def __init__(self, min_value: Any, max_value: Any):
        self.min_value = min_value
        self.max_value = max_value

    def raise_error(self, value: Any):
        """
        raises a standardised error, no need for duplications

        """
        min_msg = f"minimum: {self.min_value}" if self.min_value is not None else ""
        max_msg = f"maximum: {self.max_value}" if self.max_value is not None else ""
        raise error.PropertyValidationError(
            f"Range validation failed. value is '{value}'. {min_msg} {max_msg}"
        )

    def validate(self, value: Any):
        """
        ensures that value is between self.min_value and self.max_value

        """
        value = self.mod_value(value)
        if self.min_value:
            min_value = utils.maybe_call(self.min_value)
            min_value = self.mod_param(min_value)
            if value < min_value:
                self.raise_error(value)
        if self.max_value:
            max_value = utils.maybe_call(self.max_value)
            max_value = self.mod_param(max_value)
            if value > max_value:
                self.raise_error(value)

    def mod_value(self, value: Any) -> Any:
        """
        used by sub-classes to modify the input value

        """
        return value

    def mod_param(self, param: Any) -> Any:
        """
        used by sub-classes to modify the param value

        """
        return param


class SizeRangeCheck(RangeCheck):
    """
    ensures that a 'sized' value is within a defined range.

    >>> check = SizeRangeCheck(min_value=2, max_value=4)
    >>> check.validate(['a', 'b', 'c'])

    >>> check.validate(['a', 'b', 'c', 'd', 'e'])
    Traceback (most recent call last):
        ...
     jason.props.error.PropertyValidationError: Range validation failed. value is '5'. minimum: 2 maximum: 4

    >>> check.validate(['a'])
    Traceback (most recent call last):
        ...
     jason.props.error.PropertyValidationError: Range validation failed. value is '1'. minimum: 2 maximum: 4
    """

    def mod_value(self, value: Any) -> int:
        """
        makes _RangeCheck compare the array length

        """
        return len(value)


class DateTimeRangeCheck(RangeCheck):
    """
    ensures that a 'sized' value is within a defined range.

    >>> check = DateTimeRangeCheck(
    ...     min_value=datetime.datetime.fromisoformat("2000-01-01T00:00:00.000+00:00"),
    ...     max_value=datetime.datetime.fromisoformat("2002-01-01T00:00:00.000+00:00")
    ... )
    >>> check.validate(datetime.datetime.fromisoformat("2001-01-01T00:00:00.000+00:00"))

    >>> check.validate(datetime.datetime.fromisoformat("2003-01-01T00:00:00.000+00:00"))
    Traceback (most recent call last):
        ...
     jason.props.error.PropertyValidationError: Range validation failed. value is '2003-01-01 00:00:00+00:00'. minimum: 2000-01-01 00:00:00+00:00 maximum: 2002-01-01 00:00:00+00:00
    >>> check.validate(datetime.datetime.fromisoformat("1999-01-01T00:00:00.000+00:00"))
    Traceback (most recent call last):
        ...
     jason.props.error.PropertyValidationError: Range validation failed. value is '1999-01-01 00:00:00+00:00'. minimum: 2000-01-01 00:00:00+00:00 maximum: 2002-01-01 00:00:00+00:00
    """

    def mod_param(
        self, param: Union[datetime.datetime, datetime.date]
    ) -> Union[datetime.datetime, datetime.date]:
        """
        if no timezone is provided, assume UTC

        """
        if param.tzinfo is None:
            param = param.replace(tzinfo=datetime.timezone.utc)
        return param
