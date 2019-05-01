from typing import Any, Dict, Type, Union

from .. import base, error, utils
from .inline import Inline
from .model import Model
from .nested import Nested
from .property import Property


class Compound(Inline):
    def __init__(
        self,
        *objects: Union[Model, Nested, Dict[str, Property], Type[Model]],
        **kwargs: Any,
    ):
        schema = {}
        for obj in objects:
            if utils.is_instance_or_type(obj, Model):
                props = obj.__props__
            elif utils.is_instance_or_type(obj, (Nested, Inline)):
                props = obj.props
            elif isinstance(obj, dict):
                props = obj
            else:
                if not utils.is_type(obj):
                    obj = type(obj)
                raise ValueError(
                    f"can only combine objects of type: "
                    f"'Model', 'Inline', 'Nested'. Not '{obj}'"
                )
            for key, value in props.items():
                if not utils.is_instance_or_type(value, (Model, base.SchemaAttribute)):
                    if not utils.is_type(value):
                        value = type(value)
                    raise error.PropertyValidationError(
                        f"can only combine objects of type: "
                        f"'Model', 'SchemaAttribute'. Not '{value}'"
                    )
                if key in schema:
                    raise error.PropertyValidationError(
                        f"A property with name '{key}' already exists in combined object."
                    )
                schema[key] = value
        super(Compound, self).__init__(props=schema, **kwargs)