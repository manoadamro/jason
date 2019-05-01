import datetime
from typing import Any, Union

from . import error, utils


class RangeCheck:
    def __init__(self, min_value: Any, max_value: Any):
        self.min_value = min_value
        self.max_value = max_value

    def raise_error(self, value: Any):
        min_msg = f"minimum: {self.min_value}" if self.min_value is not None else ""
        max_msg = f"maximum: {self.max_value}" if self.max_value is not None else ""
        raise error.PropertyValidationError(
            f"Range validation failed. value is '{value}'. {min_msg} {max_msg}"
        )

    def validate(self, value: Any):
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
        return value

    def mod_param(self, param: Any) -> Any:
        return param


class SizeRangeCheck(RangeCheck):
    def mod_value(self, value: Any) -> int:
        return len(value)


class DateTimeRangeCheck(RangeCheck):
    def mod_param(
        self, param: Union[datetime.datetime, datetime.date]
    ) -> Union[datetime.datetime, datetime.date]:
        if param.tzinfo is None:
            param = param.replace(tzinfo=datetime.timezone.utc)
        return param
