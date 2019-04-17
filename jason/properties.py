import re
import uuid

from . import exceptions


class Property:
    def __init__(self, nullable=False, default=None, types=None):
        self.nullable = nullable
        self.default = default
        self.types = types

    @classmethod
    def _resolve(cls, value):
        if callable(value):
            return value()
        return value

    def load(self, value):
        if value is None:
            value = self._resolve(value=self.default)
            print(value)
        if value is None:
            if not self.nullable:
                raise exceptions.PropertyValidationError  # TODO
            return None
        if self.types and not isinstance(value, self.types):
            raise exceptions.PropertyValidationError  # TODO
        return self._validate(value)

    def _validate(self, value):
        return value

    def __call__(self, func):
        base_validator = self._validate

        def wrapped_validator(value):
            value = base_validator(value)
            return func(value)

        self._validate = wrapped_validator
        return self


class Bool(Property):
    def __init__(self, nullable=False, default=None, allow_strings=True):
        super(Bool, self).__init__(
            nullable=nullable, default=default, types=(str, bool)
        )
        self.allow_strings = allow_strings

    def _validate(self, value):
        if isinstance(value, str):
            if not self.allow_strings:
                raise exceptions.PropertyValidationError  # TODO
            value = value.lower()
            if value == "true":
                value = True
            elif value == "false":
                value = False
            else:
                raise exceptions.PropertyValidationError  # TODO
        return value


class Number(Property):
    def __init__(
        self,
        min_value=None,
        max_value=None,
        nullable=False,
        default=None,
        types=(int, float),
    ):
        super(Number, self).__init__(nullable=nullable, default=default, types=types)
        self.min_value = min_value
        self.max_value = max_value

    def _validate(self, value):
        if self.min_value:
            min_value = self._resolve(self.min_value)
            if value < min_value:
                raise exceptions.PropertyValidationError  # TODO
        if self.max_value:
            max_value = self._resolve(self.max_value)
            if value > max_value:
                raise exceptions.PropertyValidationError  # TODO
        return value


class Int(Number):
    def __init__(self, min_value=None, max_value=None, nullable=False, default=None):
        super(Int, self).__init__(
            min_value, max_value, nullable=nullable, default=default, types=(int,)
        )


class Float(Number):
    def __init__(self, min_value=None, max_value=None, nullable=False, default=None):
        super(Float, self).__init__(
            min_value, max_value, nullable=nullable, default=default, types=(int, float)
        )

    def _validate(self, value):
        value = super(Float, self)._validate(value)
        return float(value)


class String(Property):
    def __init__(self, min_length=None, max_length=None, nullable=False, default=None):
        super(String, self).__init__(nullable=nullable, default=default, types=(str,))
        self.min_length = min_length
        self.max_length = max_length

    def _validate(self, value):
        length = len(value)
        if self.min_length:
            min_length = self._resolve(self.min_length)
            if length < min_length:
                raise exceptions.PropertyValidationError  # TODO
        if self.max_length:
            max_length = self._resolve(self.max_length)
            if length > max_length:
                raise exceptions.PropertyValidationError  # TODO
        return value


class Regex(String):
    def __init__(self, matcher, nullable=False, default=None):
        super(Regex, self).__init__(nullable=nullable, default=default)
        if isinstance(matcher, str):
            matcher = re.compile(matcher)
        self.matcher = matcher

    def _validate(self, value):
        if re.match(self.matcher, value) is None:
            raise exceptions.PropertyValidationError  # TODO
        return value


class Uuid(String):
    def __init__(self, nullable=False, default=None):
        super(Uuid, self).__init__(nullable=nullable, default=default)

    def _validate(self, value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise exceptions.PropertyValidationError  # TODO
        return value


class Date(Property):
    def __init__(self, min_value=None, max_value=None, nullable=False, default=None):
        super(Date, self).__init__(nullable=nullable, default=default)
        self.min_value = min_value
        self.max_value = max_value

    def _validate(self, value):
        # TODO
        ...


class Datetime(Property):
    def __init__(self, min_value=None, max_value=None, nullable=False, default=None):
        super(Datetime, self).__init__(nullable=nullable, default=default)
        self.min_value = min_value
        self.max_value = max_value

    def _validate(self, value):
        # TODO
        ...


class Password(String):
    def __init__(self, min_length=None, max_length=None, nullable=False, default=None):
        super(Password, self).__init__(
            min_length=min_length,
            max_length=max_length,
            nullable=nullable,
            default=default,
        )

    def _validate(self, value):
        # TODO
        ...
