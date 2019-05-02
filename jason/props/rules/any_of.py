from typing import Any, Type, Union

from .. import base, error, utils


class AnyOf(base.SchemaRule):
    def __init__(self, *rules: Union[base.SchemaAttribute, Type[base.SchemaAttribute]]):
        self.rules = rules

    def load(self, value: Any) -> Any:
        errors = []
        for rule in self.rules:
            if utils.is_type(rule):
                rule = rule()
            try:
                return rule.load(value)
            except error.PropertyValidationError as ex:
                errors.append(f"could not validate against '{rule}': {ex}")
                continue
        raise error.BatchValidationError(
            f"AllOf failed to validate value '{value}' with any rules", errors
        )
