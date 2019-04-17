import re


class Property:
    def __init__(self, nullable=False, default=None, types=None):
        self.nullable = nullable
        self.default = default
        self.types = types

    @classmethod
    def _get(cls, value):
        if callable(value):
            return value()
        return value

    def load(self, value):
        if value is None:
            value = self._get(value=self.default)
        if value is None:
            if not self.nullable:
                raise Exception  # TODO
            return None
        if self.types and not isinstance(value, self.types):
            raise Exception  # TODO
        return self.validate(value)

    def validate(self, value):
        return value

    def __call__(self, func):
        def wrapped(value):
            value = self.load(value)
            return func(value)
        return wrapped


class Bool(Property):
    def __init__(self, nullable=False, default=None, allow_strings=True):
        super(Bool, self).__init__(nullable=nullable, default=default, types=(str, bool))
        self.allow_strings = allow_strings

    def validate(self, value):
        if isinstance(value, str):
            if not self.allow_strings:
                raise Exception  # TODO
            value = value.lower()
            if value == 'true':
                value = True
            elif value == 'false':
                value = False
            else:
                raise Exception  # TODO
        return value


class Number(Property):
    def __init__(self, min_value, max_value, nullable=False, default=None, types=(int, float)):
        super(Number, self).__init__(nullable=nullable, default=default, types=types)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        if self.min_value:
            min_value = self._get(self.min_value)
            if value < min_value:
                raise Exception  # TODO
        if self.max_value:
            max_value = self._get(self.max_value)
            if value > max_value:
                raise Exception  # TODO
        return value


class Int(Number):
    def __init__(self, min_value=None, max_value=None, nullable=False, default=None):
        super(Int, self).__init__(min_value, max_value, nullable=nullable, default=default, types=(int,))


class Float(Number):
    def __init__(self, min_value=None, max_value=None, nullable=False, default=None):
        super(Float, self).__init__(min_value, max_value, nullable=nullable, default=default, types=(int, float))

    def validate(self, value):
        value = super(Float, self).validate(value)
        return float(value)


class String(Property):
    def __init__(self, min_length=None, max_length=None, nullable=False, default=None):
        super(String, self).__init__(nullable=nullable, default=default, types=(str,))
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value):
        length = len(value)
        if self.min_length:
            min_length = self._get(self.min_length)
            if length < min_length:
                raise Exception  # TODO
        if self.max_length:
            max_length = self._get(self.max_length)
            if length > max_length:
                raise Exception  # TODO
        return value


class Regex(String):
    def __init__(self, matcher):
        super(Regex, self).__init__()
        self.matcher = matcher

    def validate(self, value):
        if re.match(self.matcher, value) is None:
            raise NotImplemented  # TODO
        return value
