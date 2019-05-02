import os
from typing import Any

from jason.props import error, types


class ConfigObject(types.Model):
    @classmethod
    def load(cls, **fields: Any) -> "ConfigObject":
        instance = cls()
        errors = []
        fields = {name.lower(): value for name, value in fields.items()}
        for name, prop in cls.__props__.items():
            value = fields.get(name.lower(), None)
            if value is None:
                value = os.environ.get(name.upper(), None)
            try:
                value = prop.load(value)
            except error.PropertyValidationError as ex:
                errors.append(f"could not load property '{name}': {ex}")
                continue
            setattr(instance, name, value)
        if len(errors):
            raise error.BatchValidationError("Failed to load config", errors)
        return instance

    def __getattribute__(self, item):
        try:
            return super(ConfigObject, self).__getattribute__(item)
        except AttributeError:
            return getattr(self.__dict__, item)

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__dict__[key] = value
