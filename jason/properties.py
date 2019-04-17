import datetime
import re
import uuid

from . import utils


class PropertyValidationError(Exception):
    ...


class RangeCheck:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def raise_error(self):
        raise PropertyValidationError  # TODO

    def validate(self, value):
        if self.min_value:
            min_length = utils.maybe_call(self.min_value)
            if value < min_length:
                self.raise_error()
        if self.max_value:
            max_length = utils.maybe_call(self.max_value)
            if value > max_length:
                self.raise_error()


class Property:
    def __init__(self, nullable=False, default=None, types=None):
        self.nullable = nullable
        self.default = default
        self.types = types

    def load(self, value):
        if value is None:
            value = utils.maybe_call(value=self.default)
            print(value)
        if value is None:
            if not self.nullable:
                raise PropertyValidationError  # TODO
            return None
        if self.types and not isinstance(value, self.types):
            raise PropertyValidationError  # TODO
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


class Model(Property):
    __strict__ = True
    __props__ = None

    def __init_subclass__(cls):
        props = {}
        for field in dir(cls):
            if field.startswith("_"):
                continue
            value = getattr(cls, field)
            if isinstance(value, type) and issubclass(value, Property):
                props[field] = value()
            if isinstance(value, Property):
                props[field] = value
        cls.__props__ = props


class Array(Property):
    def __init__(self, prop, min_length=None, max_length=None, **kwargs):
        if isinstance(prop, type):
            prop = prop()
        super(Array, self).__init__(types=(list, tuple), **kwargs)
        self.range = RangeCheck(min_value=min_length, max_value=max_length)
        self.prop = prop

    def _validate(self, value):
        length = len(value)
        self.range.validate(length)
        return [self.prop.load(item) for item in value]


class Nested(Property):
    def __init__(self, model, strict=None, **kwargs):
        super(Nested, self).__init__(types=(dict,), **kwargs)
        self.props = model.__props__
        if strict is None:
            strict = getattr(model, "__strict__")
        self.strict = strict

    def _validate(self, obj):
        validated = {}
        for field, prop in self.props.items():
            value = obj.get(field, None)
            validated[field] = prop.load(value)
        if self.strict:
            for field in obj:
                if field not in self.props:
                    raise PropertyValidationError  # TODO
        return validated


class Object(Model, Nested):
    def __init__(self, props, **kwargs):
        for key, value in props.items():
            if isinstance(value, type):
                props[key] = value()
        self.__props__ = props
        Nested.__init__(self, model=self, **kwargs)


class Bool(Property):
    def __init__(self, allow_strings=True, **kwargs):
        super(Bool, self).__init__(types=(str, bool), **kwargs)
        self.allow_strings = allow_strings

    def _from_string(self, value):
        if not self.allow_strings:
            raise PropertyValidationError  # TODO
        value = value.lower()
        if value == "true":
            value = True
        elif value == "false":
            value = False
        else:
            raise PropertyValidationError  # TODO
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
        self.range = RangeCheck(min_value=min_value, max_value=max_value)
        self.allow_strings = allow_strings

    def _from_string(self, value):
        if not self.allow_strings:
            raise PropertyValidationError  # TODO
        if "." in value and value.replace(".", "", 1).isnumeric():
            value = float(value)
        elif value.isnumeric():
            value = int(value)
        else:
            raise PropertyValidationError  # TODO
        return value

    def _validate(self, value):
        if isinstance(value, str):
            value = self._from_string(value)
        self.range.validate(value)
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
        self.range = RangeCheck(min_value=min_length, max_value=max_length)

    def _validate(self, value):
        length = len(value)
        self.range.validate(length)
        return value


class Regex(String):
    def __init__(self, matcher, **kwargs):
        super(Regex, self).__init__(**kwargs)
        if isinstance(matcher, str):
            matcher = re.compile(matcher)
        self.matcher = matcher

    def _validate(self, value):
        if re.match(self.matcher, value) is None:
            raise PropertyValidationError  # TODO
        return value


class Uuid(String):
    def __init__(self, **kwargs):
        super(Uuid, self).__init__(**kwargs)

    def _validate(self, value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise PropertyValidationError  # TODO
        return value


class Date(Property):
    def __init__(self, min_value=None, max_value=None, allow_strings=True, **kwargs):
        super(Date, self).__init__(types=(datetime.date, str), **kwargs)
        self.range = RangeCheck(min_value=min_value, max_value=max_value)
        self.allow_strings = allow_strings

    def _from_string(self, value):
        if not self.allow_strings:
            raise PropertyValidationError  # TODO
        try:
            value = datetime.date.fromisoformat(value)
        except ValueError:
            raise PropertyValidationError  # TODO
        return value

    def _validate(self, value):
        if isinstance(value, str):
            value = self._from_string(value)
        self.range.validate(value)
        return value


class Datetime(Property):
    def __init__(self, min_value=None, max_value=None, allow_strings=True, **kwargs):
        super(Datetime, self).__init__(types=(datetime.datetime, str), **kwargs)
        self.range = RangeCheck(min_value=min_value, max_value=max_value)
        self.allow_strings = allow_strings

    def _from_string(self, value):
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        if not self.allow_strings:
            raise PropertyValidationError  # TODO
        try:
            value = datetime.datetime.fromisoformat(value)
        except ValueError:
            raise PropertyValidationError  # TODO
        return value

    def _validate(self, value):
        if isinstance(value, str):
            value = self._from_string(value)
        self.range.validate(value)
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
            raise PropertyValidationError  # TODO

        if re.search(self.uppercase_matcher, value):
            if self.uppercase is False:
                raise PropertyValidationError  # TODO
            score += 1
        elif self.uppercase is True:
            raise PropertyValidationError  # TODO

        if re.search(self.numbers_matcher, value):
            if self.numbers is False:
                raise PropertyValidationError  # TODO
            score += 1
        elif self.numbers is True:
            raise PropertyValidationError  # TODO

        if re.search(self.symbols_matcher, value):
            if self.symbols is False:
                raise PropertyValidationError  # TODO
            score += 1
        elif self.symbols is True:
            raise PropertyValidationError  # TODO

        if score < self.min_score:
            raise PropertyValidationError  # TODO

        return value


class Email(Regex):
    matcher = re.compile("^[^@]+@[^@]+\\.[^@]+$")

    def __init__(self, **kwargs):
        super(Email, self).__init__(self.matcher, **kwargs)
