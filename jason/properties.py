import datetime
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
    def __init__(self, allow_strings=True, **kwargs):
        super(Bool, self).__init__(types=(str, bool), **kwargs)
        self.allow_strings = allow_strings

    def _from_string(self, value):
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

    def _validate(self, value):
        if isinstance(value, str):
            value = self._from_string(value)
        return value


class Number(Property):
    def __init__(
        self,
        min_value=None,
        max_value=None,
        allow_strings=True,
        types=(int, float, str),
        **kwargs
    ):
        super(Number, self).__init__(types=types, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.allow_strings = allow_strings

    def _from_string(self, value):
        if not self.allow_strings:
            raise exceptions.PropertyValidationError  # TODO
        if "." in value and value.replace(".", "", 1).isnumeric():
            value = float(value)
        elif value.isnumeric():
            value = int(value)
        else:
            raise exceptions.PropertyValidationError  # TODO
        return value

    def _validate(self, value):
        if isinstance(value, str):
            value = self._from_string(value)
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
    def __init__(self, **kwargs):
        super(Int, self).__init__(types=(str, int), **kwargs)


class Float(Number):
    def __init__(self, **kwargs):
        super(Float, self).__init__(types=(str, int, float), **kwargs)

    def _validate(self, value):
        value = super(Float, self)._validate(value)
        return float(value)


class String(Property):
    def __init__(self, min_length=None, max_length=None, **kwargs):
        super(String, self).__init__(types=(str,), **kwargs)
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
    def __init__(self, matcher, **kwargs):
        super(Regex, self).__init__(**kwargs)
        if isinstance(matcher, str):
            matcher = re.compile(matcher)
        self.matcher = matcher

    def _validate(self, value):
        if re.match(self.matcher, value) is None:
            raise exceptions.PropertyValidationError  # TODO
        return value


class Uuid(String):
    def __init__(self, **kwargs):
        super(Uuid, self).__init__(**kwargs)

    def _validate(self, value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise exceptions.PropertyValidationError  # TODO
        return value


class Date(Property):
    def __init__(self, min_value=None, max_value=None, allow_strings=True, **kwargs):
        super(Date, self).__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.allow_strings = allow_strings

    def _from_string(self, value):
        if not self.allow_strings:
            raise exceptions.PropertyValidationError  # TODO
        try:
            value = datetime.date.fromisoformat(value)
        except ValueError:
            raise exceptions.PropertyValidationError  # TODO
        return value

    def _validate(self, value):
        if isinstance(value, str):
            value = self._from_string(value)
        if self.min_value:
            min_value = self._resolve(self.min_value)
            if value < min_value:
                raise exceptions.PropertyValidationError  # TODO
        if self.max_value:
            max_value = self._resolve(self.max_value)
            if value > max_value:
                raise exceptions.PropertyValidationError  # TODO
        return value


class Datetime(Property):
    def __init__(self, min_value=None, max_value=None, allow_strings=True, **kwargs):
        super(Datetime, self).__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.allow_strings = allow_strings

    def _from_string(self, value):
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        if not self.allow_strings:
            raise exceptions.PropertyValidationError  # TODO
        try:
            value = datetime.datetime.fromisoformat(value)
        except ValueError:
            raise exceptions.PropertyValidationError  # TODO
        return value

    def _validate(self, value):
        if isinstance(value, str):
            value = self._from_string(value)
        if self.min_value:
            min_value = self._resolve(self.min_value)
            if value < min_value:
                raise exceptions.PropertyValidationError  # TODO
        if self.max_value:
            max_value = self._resolve(self.max_value)
            if value > max_value:
                raise exceptions.PropertyValidationError  # TODO
        return value


class Password(String):
    uppercase_matcher = re.compile("[A-Z]")
    numbers_matcher = re.compile("[0-9]")
    symbols_matcher = re.compile("[^A-Za-z0-9]")
    whitespace_matcher = re.compile("[\\s]")

    def __init__(self, uppercase=None, numbers=None, symbols=None, score=0, **kwargs):
        super(Password, self).__init__(**kwargs)
        self.uppercase = uppercase
        self.numbers = numbers
        self.symbols = symbols
        self.min_score = score

    def _validate(self, value):

        score = 0
        if re.search(self.whitespace_matcher, value):
            raise exceptions.PropertyValidationError  # TODO

        if re.search(self.uppercase_matcher, value):
            if self.uppercase is False:
                raise exceptions.PropertyValidationError  # TODO
            score += 1
        elif self.uppercase is True:
            raise exceptions.PropertyValidationError  # TODO

        if re.search(self.numbers_matcher, value):
            if self.numbers is False:
                raise exceptions.PropertyValidationError  # TODO
            score += 1
        elif self.numbers is True:
            raise exceptions.PropertyValidationError  # TODO

        if re.search(self.symbols_matcher, value):
            if self.symbols is False:
                raise exceptions.PropertyValidationError  # TODO
            score += 1
        elif self.symbols is True:
            raise exceptions.PropertyValidationError  # TODO

        if score < self.min_score:
            raise exceptions.PropertyValidationError  # TODO

        return value


class Email(Regex):
    matcher = re.compile("^[^@]+@[^@]+\\.[^@]+$")

    def __init__(self, **kwargs):
        super(Email, self).__init__(self.matcher, **kwargs)


class Array(Property):
    ...  # TODO


class Object(Property):
    ...  # TODO


class Model(Property):
    ...  # TODO
