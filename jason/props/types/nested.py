from typing import Any, Dict, Type, Union

from .. import error
from .model import Model
from .property import Property


class Nested(Property):
    def __init__(
        self, model: Union[Type[Model], Model], strict: bool = None, **kwargs: Any
    ):
        super(Nested, self).__init__(types=(dict,), **kwargs)
        self.props = model.__props__
        if strict is None:
            strict = getattr(model, "__strict__")
        self.strict = strict

    def _validate(self, obj: Dict[Any, Any]) -> Dict[Any, Any]:

        validated = {}
        errors = []
        for field, prop in self.props.items():
            value = obj.get(field, None)
            try:
                validated[field] = prop.load(value)
            except error.PropertyValidationError as ex:
                errors.append(f"could not load property '{field}': {ex}")
                continue
        if self.strict:
            extras = [k for k in obj if k not in self.props]
            if len(extras):
                errors.append(
                    f"Strict mode is True and supplied object contains extra keys: "
                    f"'{', '.join(extras)}'"
                )
        if errors:
            raise error.BatchValidationError(
                f"failed to validate {obj} against {self}", errors
            )
        return validated
