import datetime
from typing import Union

from .range import RangeCheck


class DateTimeRangeCheck(RangeCheck):
    def _mod(
        self, param: Union[datetime.datetime, datetime.date, str]
    ) -> Union[datetime.datetime, datetime.date]:
        if isinstance(param, str):
            if param.endswith("Z"):
                param = f"{param[:-1]}+00:00"
            try:
                param = datetime.date.fromisoformat(param)
            except ValueError:
                param = datetime.datetime.fromisoformat(param)
        if isinstance(param, datetime.datetime) and param.tzinfo is None:
            param = param.replace(tzinfo=datetime.timezone.utc)
        return param

    def mod_param(
        self, param: Union[datetime.datetime, datetime.date, str]
    ) -> Union[datetime.datetime, datetime.date]:

        return self._mod(param)

    def mod_value(
        self, param: Union[datetime.datetime, datetime.date, str]
    ) -> Union[datetime.datetime, datetime.date]:

        return self._mod(param)
