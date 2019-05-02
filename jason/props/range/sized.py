from typing import Any

from .range import RangeCheck


class SizeRangeCheck(RangeCheck):
    def mod_value(self, value: Any) -> int:
        return len(value)
