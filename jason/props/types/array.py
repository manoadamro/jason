from typing import Any, Callable, List, Tuple, Type, Union

from .. import base, error, range
from .property import Property


class Array(Property):
    def __init__(
        self,
        prop: Union[base.SchemaAttribute, Type[base.SchemaAttribute]],
        min_length: Union[int, Callable[[], int]] = None,
        max_length: Union[int, Callable[[], int]] = None,
        **kwargs: Any,
    ):
        if isinstance(prop, type):
            prop = prop()
        super(Array, self).__init__(types=(list, tuple), **kwargs)
        self.range = range.SizeRangeCheck(min_value=min_length, max_value=max_length)
        self.prop = prop

    def _validate(self, value: Union[List, Tuple]) -> Union[List, Tuple]:

        self.range.validate(value)
        errors = []
        validated = []
        for item in value:
            try:
                value = self.prop.load(item)
            except error.PropertyValidationError as ex:
                errors.append(f"could not validate {value}: {ex}")
                continue
            validated.append(value)
        if errors:
            raise error.BatchValidationError(
                f"failed to validate {value} against {self}", errors
            )
        return validated
