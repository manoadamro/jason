from typing import Any, Dict, Type, Union

from .. import base
from .model import Model
from .nested import Nested


class Inline(Model, Nested):
    def __init__(
        self,
        props: Dict[
            str,
            Union[Model, base.SchemaAttribute, Type[Model], Type[base.SchemaAttribute]],
        ],
        **kwargs: Any,
    ):
        for key, value in props.items():
            if isinstance(value, type):
                props[key] = value()
        self.__props__ = props
        Nested.__init__(self, model=self, **kwargs)
