import datetime
from typing import Union

from .range import RangeCheck


class DateTimeRangeCheck(RangeCheck):
    def mod_param(
        self, param: Union[datetime.datetime, datetime.date]
    ) -> Union[datetime.datetime, datetime.date]:
        if param.tzinfo is None:
            param = param.replace(tzinfo=datetime.timezone.utc)
        return param
