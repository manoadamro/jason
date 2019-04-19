"""
config

"""
import os
from typing import Any

from . import schema as _schema

props = _schema


class Config(props.Model):
    """
    attempts to load values first from the 'fields' parameter and if `None`, from the env.

    >>> class MyConfig(Config):
    ...    MY_INT = props.Int()
    ...    MY_FLOAT = props.Float()
    ...    MY_STRING = props.String()
    ...    MY_BOOL = props.Bool()

    assume os.environ looks like this:
    >>> os.environ = {"MY_INT": "123", "MY_FLOAT": "12.3", "MY_STRING": "stringy", "MY_BOOL": "true",}

    we can pass in MY_STRING (in upper or lower case) to override the environment variable
    MY_INT, MY_FLOAT, MY_BOOL will be taken from env
    >>> config = MyConfig.load(my_string="something")

    >>> config.MY_STRING
    'something'

    >>> config.MY_FLOAT
    12.3

    """

    @classmethod
    def load(cls, **fields: Any) -> "Config":
        """
        attempts to load values first from the 'fields' parameter and if `None`, from the env.
        values that do not exist in either place will default to `None`
        validated values are added to the instance.

        """
        instance = cls()
        fields = {name.lower(): value for name, value in fields.items()}
        for name, prop in cls.__props__.items():
            value = fields.get(name.lower(), None)
            if value is None:
                value = os.environ.get(name.upper(), None)
            value = prop.load(value)
            setattr(instance, name, value)
        return instance
