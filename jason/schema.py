"""
schema

"""
import datetime
import re
import uuid
from typing import Any, Callable, Dict, List, Pattern, Tuple, Type, Union

from . import utils


class PropertyValidationError(Exception):
    """
    raised when a property fails to validate a value

    """

    ...


class SchemaAttribute:
    """
    base class for all schema schema and rules

    """

    def load(self, value: Any) -> Any:
        """
        Must be overridden in sub-classes

        """
        raise NotImplementedError


class AnyOf(SchemaAttribute):
    """
    takes an unpacked tuple of schema attributes
    and ensures that the value conforms to at least one of them

    The value is returned from the first attribute that does not raise a PropertyValidationError.
    If the value matches none of them, a PropertyValidationError is raised.

    >>> rule = AnyOf(Property(types=(int, float)), Property(types=(str,)))
    >>> rule.load("hello")
    'hello'
    >>> rule.load(True)
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: AllOf failed to validate value 'True' with any rules

    """

    def __init__(self, *rules: Union[SchemaAttribute, Type[SchemaAttribute]]):
        self.rules = rules

    def load(self, value: Any) -> Any:
        """
        ensures that a value can be loaded by at least one of the defined rules (schema attributes)
        as soon as one loads without raising an error, the loaded value is returned.

        If the value fails to be loaded by any of them, a PropertyValidationError is raised.

        """
        for rule in self.rules:
            if utils.is_type(rule):
                rule = rule()
            try:
                return rule.load(value)
            except PropertyValidationError:
                continue
        raise PropertyValidationError(
            f"AllOf failed to validate value '{value}' with any rules"
        )


class Property(SchemaAttribute):
    """
    Base class for all schema schema.
    validates type against a whitelist,
    validates nullability,
    resolves from default where applicable

    :param nullable: if True, and a value is None,
    it will try to load from default and if still none,
    the rest of the validation will be skipped.

    >>> prop = Property(nullable=False)
    >>> prop.load(None)
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Property is not nullable

    >>> prop = Property(nullable=True)
    >>> prop.load(None)

    :param default: if a null value is received, this value will be used in it's place.
    default can be an arg-less callable and it's return value will be used.

    >>> prop = Property(default=123)
    >>> prop.load(None)
    123

    >>> prop = Property(default=lambda: 123)
    >>> prop.load(None)
    123

    :param types: a white list of types.
    If empty, there will be no type validation,
    otherwise the value must be of a type defined in this collection.

    >>> prop = Property(types=(int,))
    >>> prop.load(123)
    123

    >>> prop = Property(types=(int,))
    >>> prop.load("nope")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Property was expected to be of type: int. not str
    """

    def __init__(
        self,
        nullable: bool = False,
        default: Any = None,
        types: Union[Tuple[Type, ...], List[Type]] = None,
    ):
        self.nullable = nullable
        self.default = default
        self.types = types

    def load(self, value: Any) -> Any:
        """
        Attempts to validate a value based on the defined rules.
        The validated value is always returned if an error is not raised.

        If the value can not be validated a PropertyValidationError is raised.

        """
        if value is None:
            value = utils.maybe_call(value=self.default)
        if value is None:
            if not self.nullable:
                raise PropertyValidationError(f"Property is not nullable")
            return None
        if self.types and (
            (utils.is_bool(value) and bool not in self.types)
            or not isinstance(value, self.types)
        ):
            raise PropertyValidationError(
                f"Property was expected to be of type: {', '.join(t.__name__ for t in self.types)}. not {type(value).__name__}"
            )
        return self._validate(value)

    def _validate(self, value: Any) -> Any:
        """
        overridden by sub-classes

        """
        return value

    def __call__(self, func: Callable[[Any], Any]) -> "Property":
        """
        allows property to be used as decorator.
        validation will be carried out on supplied value as normal
        then decorated method is called with the validated value.

        whatever the decorated method returns will be considered the final validated value.

        """
        base_validator = self._validate

        def wrapped_validator(value: Any) -> Any:
            """
            carries out the normal property validation,
            then calls the decorated method for custom validation.
            """
            value = base_validator(value)
            return func(value)

        self._validate = wrapped_validator
        return self


class Model:
    """
    Base class for schema models.
    Will auto load schema when sub-class is initialised.

    >>> class MyModel(Model):
    ...     my_int = Property()
    ...     my_str = Property()
    >>> MyModel.__props__
    {'my_int': <jason.schema.Property object at 0x...>, 'my_str': <jason.schema.Property object at 0x...>}

    By default, the __strict__ field will default to True
    >>> MyModel.__strict__
    True

    """

    __strict__ = True
    __props__ = None

    def __init_subclass__(cls):
        """
        Every time a sub-class is initialised, the schema are loaded into a dictionary.
        This saves a lot of overhead compared to doing it on the fly each time.

        """
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
    """
    Validates that each value in a list or tuple conforms to the rule defined by the 'prop' parameter.

    :parameter prop: the property or rule to validate each value against.
    :parameter min_length: the minimum length of the array. set None to skip this validation
    :parameter max_length: the maximum length of the array. set None to skip this validation

    (see 'Property' definition for basic parameters)

    >>> arr = Array(Property(nullable=False, types=(str,)), min_length=2, max_length=3)
    >>> arr.load(["a", "b", "c"])
    ['a', 'b', 'c']

    >>> arr.load(["a", 2, "c"])
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Property was expected to be of type: str. not int

    >>> arr.load(["a"])
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Range validation failed. value is '1'. minimum: 2 maximum: 3

    >>> arr.load(["a", "b", "c", "d"])
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Range validation failed. value is '4'. minimum: 2 maximum: 3
    """

    def __init__(
        self,
        prop: Union[SchemaAttribute, Type[SchemaAttribute]],
        min_length: Union[int, Callable[[], int]] = None,
        max_length: Union[int, Callable[[], int]] = None,
        **kwargs: Any,
    ):
        if isinstance(prop, type):
            prop = prop()
        super(Array, self).__init__(types=(list, tuple), **kwargs)
        self.range = SizeRangeCheck(min_value=min_length, max_value=max_length)
        self.prop = prop

    def _validate(self, value: Union[List, Tuple]) -> Union[List, Tuple]:
        """
        Validates the length of the list/tuple if applicable.

        """
        self.range.validate(value)
        return [self.prop.load(item) for item in value]


class Nested(Property):
    """
    Allows nesting of a model as a field inside another model or object

    >>> class MyModel(Model):
    ...     my_int = Property()
    ...     my_str = Property()
    >>> nested = Nested(MyModel)
    >>> nested.props
    {'my_int': <jason.schema.Property object at 0x...>, 'my_str': <jason.schema.Property object at 0x...>}

    By default, the strict field will default to True
    >>> nested.strict
    True

    """

    def __init__(
        self, model: Union[Type[Model], Model], strict: bool = None, **kwargs: Any
    ):
        super(Nested, self).__init__(types=(dict,), **kwargs)
        self.props = model.__props__
        if strict is None:
            strict = getattr(model, "__strict__")
        self.strict = strict

    def _validate(self, obj: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        Validates each field in 'obj' based on rules defined in 'self.props'

        """
        validated = {}
        for field, prop in self.props.items():
            value = obj.get(field, None)
            validated[field] = prop.load(value)
        if self.strict:
            extras = [k for k in obj if k not in self.props]
            if len(extras):
                raise PropertyValidationError(
                    f"Strict mode is True and supplied object contains extra keys: "
                    f"'{', '.join(extras)}'"
                )
        return validated


class Inline(Model, Nested):
    """
    Allows the use of nested objects without having to define a model

    >>> inline = Inline(dict(my_int=Property(), my_str=Property()))
    >>> inline.props
    {'my_int': <jason.schema.Property object at 0x...>, 'my_str': <jason.schema.Property object at 0x...>}

    can be used in place of a model:
    >>> isinstance(inline, Model)
    True

    can be used in place of a nested object:
    >>> isinstance(inline, Nested)
    True

    """

    def __init__(
        self,
        props: Dict[
            str, Union[Model, SchemaAttribute, Type[Model], Type[SchemaAttribute]]
        ],
        **kwargs: Any,
    ):
        for key, value in props.items():
            if isinstance(value, type):
                props[key] = value()
        self.__props__ = props
        Nested.__init__(self, model=self, **kwargs)


class Combine(Inline):
    """
    Combines two or more objects.
    objects must be either a Model or Property

    >>> class MyModel(Model):
    ...     my_int = Property()
    ...     my_str = Property()
    >>> inline = Inline(props=dict(my_string=String))
    >>> class NestedModel(Model):
    ...     my_bool = Bool
    >>> nested = Nested(NestedModel)
    >>> combined = Combine(MyModel, inline, nested)
    >>> combined.props
    {'my_int': <...>, 'my_str': <...>, 'my_string': <...>, 'my_bool': <...>}

    """

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
                if not utils.is_instance_or_type(value, (Model, SchemaAttribute)):
                    if not utils.is_type(value):
                        value = type(value)
                    raise PropertyValidationError(
                        f"can only combine objects of type: "
                        f"'Model', 'SchemaAttribute'. Not '{value}'"
                    )
                if key in schema:
                    raise PropertyValidationError(
                        f"A property with name '{key}' already exists in combined object."
                    )
                schema[key] = value
        super(Combine, self).__init__(props=schema, **kwargs)


class Bool(Property):
    """
    Validates a boolean value

    >>> b = Bool()
    >>> b.load(True)
    True

    >>> b.load(False)
    False

    >>> b.load(123)
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Property was expected to be of type: str, bool. not int

    >>> b.load("nope")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Could not coerce string 'nope' to boolean

    >>> b.load("true")
    True

    >>> b.load("false")
    False

    >>> b = Bool(allow_strings=False)
    >>> b.load("true")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Loading boolean from string is not allowed

    """

    def __init__(self, allow_strings: bool = True, **kwargs: Any):
        super(Bool, self).__init__(types=(str, bool), **kwargs)
        self.allow_strings = allow_strings

    def _from_string(self, value: str) -> bool:
        """
        Tries to coerce a string to a boolean (if self.allow_string is True)

        """
        if not self.allow_strings:
            raise PropertyValidationError("Loading boolean from string is not allowed")
        value = value.lower()
        if value == "true":
            value = True
        elif value == "false":
            value = False
        else:
            raise PropertyValidationError(
                f"Could not coerce string '{value}' to boolean"
            )
        return value

    def _validate(self, value: Union[str, bool]) -> bool:
        """
        will try to validated from string if applicable

        """
        if isinstance(value, str):
            value = self._from_string(value)
        return value


class Number(Property):
    """
    Validates either a float or an int value

    >>> number = Number()
    >>> number.load(123)
    123

    >>> number.load(12.3)
    12.3

    >>> number.load("123")
    123

    >>> number.load("12.3")
    12.3

    >>> number.load(True)
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Property was expected to be of type: int, float, str. not bool

    >>> number = Number(allow_strings=False)
    >>> number.load("12.3")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Loading number from string is not allowed

    """

    def __init__(
        self,
        min_value: Union[Callable[[], int], int] = None,
        max_value: Union[Callable[[], int], int] = None,
        allow_strings: bool = True,
        types: Tuple[Type, ...] = (int, float, str),
        **kwargs: Any,
    ):
        super(Number, self).__init__(types=types, **kwargs)
        self.range = RangeCheck(min_value=min_value, max_value=max_value)
        self.allow_strings = allow_strings

    def _from_string(self, value: str) -> Union[int, float]:
        """
         Tries to coerce a string to a number (if self.allow_string is True)

         """
        if not self.allow_strings:
            raise PropertyValidationError("Loading number from string is not allowed")
        if "." in value and value.replace(".", "", 1).isnumeric():
            value = float(value)
        elif value.isnumeric():
            value = int(value)
        else:
            raise PropertyValidationError(
                f"Could not coerce string '{value}' to number"
            )
        return value

    def _validate(self, value: Union[int, float, str]) -> Union[int, float]:
        """
        will check range and try to validate from string if applicable

        """
        if isinstance(value, str):
            value = self._from_string(value)
        self.range.validate(value)
        return value


class Int(Number):
    """
    Validates an int value

    >>> number = Int()
    >>> number.load(123)
    123

    >>> number.load("123")
    123

    >>> number.load(12.3)
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Property was expected to be of type: str, int. not float


    >>> number = Int(allow_strings=False)
    >>> number.load("123")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Loading number from string is not allowed

    """

    def __init__(self, **kwargs: Any):
        super(Int, self).__init__(types=(str, int), **kwargs)

    def _validate(self, value: Union[int, str]) -> int:
        return super(Int, self)._validate(value)


class Float(Number):
    """
    Validates a float value

    >>> number = Float()
    >>> number.load(123)
    123.0

    >>> number.load("123")
    123.0

    >>> number.load(12.3)
    12.3

    >>> number = Float(allow_strings=False)
    >>> number.load("12.3")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Loading number from string is not allowed

    """

    def __init__(self, **kwargs: Any):
        super(Float, self).__init__(types=(str, int, float), **kwargs)

    def _validate(self, value: Union[int, float, str]) -> float:
        """
        will cast value to float before return

        """
        value = super(Float, self)._validate(value)
        return float(value)


class String(Property):
    """
    validates a string value

    >>> string = String()
    >>> string.load("hello")
    'hello'

    >>> string.load(123)
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Property was expected to be of type: str. not int


    >>> string = String(min_length=3, max_length=5)
    >>> string.load("a")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Range validation failed. value is '1'. minimum: 3 maximum: 5


    >>> string = String(min_length=3, max_length=5)
    >>> string.load("reeeee")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Range validation failed. value is '6'. minimum: 3 maximum: 5

    """

    def __init__(
        self,
        min_length: Union[Callable[[], int], int] = None,
        max_length: Union[Callable[[], int], int] = None,
        **kwargs: Any,
    ):
        super(String, self).__init__(types=(str,), **kwargs)
        self.range = SizeRangeCheck(min_value=min_length, max_value=max_length)

    def _validate(self, value: str) -> str:
        """
        Will validate length of string using range

        """
        self.range.validate(value)
        return value


class Regex(String):
    """
    validates a string value against a defined regex matcher

    >>> regex = Regex(re.compile("^[a-zA-Z]+$"))
    >>> regex.load("hello")
    'hello'

    >>> regex.load("h3ll0")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: String value 'h3ll0' did not match regex pattern '^[a-zA-Z]+$'

    """

    def __init__(self, matcher: Union[str, Pattern], **kwargs: Any):
        super(Regex, self).__init__(**kwargs)
        if isinstance(matcher, str):
            matcher = re.compile(matcher)
        self.matcher = matcher

    def _validate(self, value: str) -> str:
        """
        will validate value against defined 'matcher'

        """
        if re.match(self.matcher, value) is None:
            raise PropertyValidationError(
                f"String value '{value}' did not match regex pattern '{self.matcher.pattern}'"
            )
        return value


class Uuid(String):
    """
    validates a string value against the uuid4 standard

    >>> uid = Uuid()
    >>> uid.load("1f174287-2bd2-46b7-ba13-ed70aa110327")
    '1f174287-2bd2-46b7-ba13-ed70aa110327'

    >>> uid.load("nope")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: value 'nope' is not a valid uuid

    """

    def __init__(self):
        super(Uuid, self).__init__()

    def _validate(self, value: str) -> str:
        """
        Will validate the supplied uuid against the uuid4 standard.

        """
        try:
            uuid.UUID(value)
        except ValueError:
            raise PropertyValidationError(f"value '{value}' is not a valid uuid")
        return value


class Date(Property):
    """
    validates a date string or object

    >>> date = Date()

    >>> date.load(datetime.date(year=1970, month=1, day=1))
    datetime.date(1970, 1, 1)

    >>> date.load("1970-01-01")
    datetime.date(1970, 1, 1)

    >>> date = Date(allow_strings=False)
    >>> date.load("1970-01-01")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Loading date from string is not allowed

    """

    def __init__(
        self,
        min_value: Union[Callable[[], int], int] = None,
        max_value: Union[Callable[[], int], int] = None,
        allow_strings: bool = True,
        **kwargs: Any,
    ):
        super(Date, self).__init__(types=(datetime.date, str), **kwargs)
        self.range = RangeCheck(min_value=min_value, max_value=max_value)
        self.allow_strings = allow_strings

    def _from_string(self, value: str) -> datetime.date:
        """
        Tries to coerce a iso8601 date string to a date object (if self.allow_string is True)

        """
        if not self.allow_strings:
            raise PropertyValidationError("Loading date from string is not allowed")
        try:
            value = datetime.date.fromisoformat(value)
        except ValueError:
            raise PropertyValidationError(
                f"Could not coerce string '{value}' to date object"
            )
        return value

    def _validate(self, value: Union[str, datetime.date]) -> datetime.date:
        """
        Will try to load value from string and validate it against the defined range if applicable
        
        """
        if isinstance(value, str):
            value = self._from_string(value)
        self.range.validate(value)
        return value


class Datetime(Property):
    """
    validates a datetime string or object

    >>> datet = Datetime()

    >>> datet.load(datetime.datetime(year=1970, month=1, day=1, hour=1, minute=1, second=1))
    datetime.datetime(1970, 1, 1, 1, 1, 1, tzinfo=datetime.timezone.utc)

    >>> datet.load("1970-01-01T01:01:01.000Z")
    datetime.datetime(1970, 1, 1, 1, 1, 1, tzinfo=datetime.timezone.utc)

    >>> datet = Datetime(allow_strings=False)
    >>> datet.load("1970-01-01T01:01:01.000Z")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Loading datetime from string is not allowed

    """

    def __init__(
        self,
        min_value: Union[Callable[[], int], int] = None,
        max_value: Union[Callable[[], int], int] = None,
        allow_strings: bool = True,
        **kwargs: Any,
    ):
        super(Datetime, self).__init__(types=(datetime.datetime, str), **kwargs)
        self.range = DateTimeRangeCheck(min_value=min_value, max_value=max_value)
        self.allow_strings = allow_strings

    def _from_string(self, value: str) -> datetime.datetime:
        """
        Tries to coerce a iso8601 datetime string to a datetime object (if self.allow_string is True)

        """
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        if not self.allow_strings:
            raise PropertyValidationError("Loading datetime from string is not allowed")
        try:
            value = datetime.datetime.fromisoformat(value)
        except ValueError:
            raise PropertyValidationError(
                f"Could not coerce string '{value}' to datetime object"
            )
        return value

    def _validate(self, value: Union[datetime.datetime, str]) -> datetime.datetime:
        """
        Will try to load value from string and validate it against the defined range if applicable

        """
        if isinstance(value, str):
            value = self._from_string(value)
        if value.tzinfo is None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        self.range.validate(value)
        return value


class Password(String):
    """
    validates a password string against defined rules

    >>> password = Password()
    >>> password.load("my password")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Password must not contain white space


    >>> password = Password(uppercase=True)
    >>> password.load("Password")
    'Password'
    >>> password.load("password")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Password must contain at least 1 uppercase character

    >>> password = Password(uppercase=False)
    >>> password.load("password")
    'password'

    >>> password.load("Password")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Password must not contain uppercase characters

    >>> password = Password(uppercase=None)
    >>> password.load("password")
    'password'

    >>> password.load("Password")
    'Password'


    >>> password = Password(numbers=True)
    >>> password.load("p4ssw0rd")
    'p4ssw0rd'
    >>> password.load("password")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Password must contain at least 1 number

    >>> password = Password(numbers=False)
    >>> password.load("password")
    'password'

    >>> password.load("p4ssw0rd")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Password must not contain numbers

    >>> password = Password(numbers=None)
    >>> password.load("password")
    'password'

    >>> password.load("p4ssw0rd")
    'p4ssw0rd'


    >>> password = Password(symbols=True)
    >>> password.load("pa$$word")
    'pa$$word'
    >>> password.load("password")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Password must contain at least 1 symbol character

    >>> password = Password(symbols=False)
    >>> password.load("password")
    'password'

    >>> password.load("pa$$word")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Password must not contain symbol characters

    >>> password = Password(symbols=None)
    >>> password.load("password")
    'password'

    >>> password.load("pa$$word")
    'pa$$word'


    >>> password = Password(score=3)
    >>> password.load("password")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Password is too weak. minimum score: 3. current score: 0

    >>> password.load("Password")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Password is too weak. minimum score: 3. current score: 1

    >>> password.load("P4ssw0rd")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Password is too weak. minimum score: 3. current score: 2

    >>> password.load("P4$$w0rd")
    'P4$$w0rd'

    """

    uppercase_matcher = re.compile("[A-Z]")
    numbers_matcher = re.compile("[0-9]")
    symbols_matcher = re.compile("[^A-Za-z0-9]")
    whitespace_matcher = re.compile("[\\s]")
    max_score = 3

    def __init__(
        self,
        uppercase: bool = None,
        numbers: bool = None,
        symbols: bool = None,
        score: int = 0,
        **kwargs: Any,
    ):
        super(Password, self).__init__(**kwargs)
        self.uppercase = uppercase
        self.numbers = numbers
        self.symbols = symbols
        self.min_score = min(score, self.max_score)

    def _validate(self, value: str) -> str:
        """
        Will validate value string against defined character and score rules

        """
        score = 0
        if re.search(self.whitespace_matcher, value):
            raise PropertyValidationError(f"Password must not contain white space")

        if re.search(self.uppercase_matcher, value):
            if self.uppercase is False:
                raise PropertyValidationError(
                    f"Password must not contain uppercase characters"
                )
            score += 1
        elif self.uppercase is True:
            raise PropertyValidationError(
                f"Password must contain at least 1 uppercase character"
            )

        if re.search(self.numbers_matcher, value):
            if self.numbers is False:
                raise PropertyValidationError(f"Password must not contain numbers")
            score += 1
        elif self.numbers is True:
            raise PropertyValidationError(f"Password must contain at least 1 number")

        if re.search(self.symbols_matcher, value):
            if self.symbols is False:
                raise PropertyValidationError(
                    f"Password must not contain symbol characters"
                )
            score += 1
        elif self.symbols is True:
            raise PropertyValidationError(
                f"Password must contain at least 1 symbol character"
            )

        if score < self.min_score:
            raise PropertyValidationError(
                f"Password is too weak. "
                f"minimum score: {self.min_score}. "
                f"current score: {score}"
            )

        return value


class Email(Regex):
    """
    Validates an email address against a basic regex matcher.

    >>> email = Email()
    >>> email.load("someone@something.com")
    'someone@something.com'

    >>> email.load("nope")
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: String value 'nope' did not match regex pattern '^[^@]+@[^@]+\\.[^@]+$'

    """

    matcher = re.compile("^[^@]+@[^@]+\\.[^@]+$")

    def __init__(self, **kwargs: Any):
        super(Email, self).__init__(self.matcher, **kwargs)


class RangeCheck:
    """
    ensures that a value is within a defined range.

    >>> check = RangeCheck(min_value=5, max_value=10)
    >>> check.validate(7)

    >>> check.validate(15)
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Range validation failed. value is '15'. minimum: 5 maximum: 10

    >>> check.validate(3)
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Range validation failed. value is '3'. minimum: 5 maximum: 10

    """

    def __init__(self, min_value: Any, max_value: Any):
        self.min_value = min_value
        self.max_value = max_value

    def raise_error(self, value: Any):
        """
        raises a standardised error, no need for duplications

        """
        min_msg = f"minimum: {self.min_value}" if self.min_value is not None else ""
        max_msg = f"maximum: {self.max_value}" if self.max_value is not None else ""
        raise PropertyValidationError(
            f"Range validation failed. value is '{value}'. {min_msg} {max_msg}"
        )

    def validate(self, value: Any):
        """
        ensures that value is between self.min_value and self.max_value

        """
        value = self.mod_value(value)
        if self.min_value:
            min_value = utils.maybe_call(self.min_value)
            min_value = self.mod_param(min_value)
            if value < min_value:
                self.raise_error(value)
        if self.max_value:
            max_value = utils.maybe_call(self.max_value)
            max_value = self.mod_param(max_value)
            if value > max_value:
                self.raise_error(value)

    def mod_value(self, value: Any) -> Any:
        """
        used by sub-classes to modify the input value

        """
        return value

    def mod_param(self, param: Any) -> Any:
        """
        used by sub-classes to modify the param value

        """
        return param


class SizeRangeCheck(RangeCheck):
    """
    ensures that a 'sized' value is within a defined range.

    >>> check = SizeRangeCheck(min_value=2, max_value=4)
    >>> check.validate(['a', 'b', 'c'])

    >>> check.validate(['a', 'b', 'c', 'd', 'e'])
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Range validation failed. value is '5'. minimum: 2 maximum: 4

    >>> check.validate(['a'])
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Range validation failed. value is '1'. minimum: 2 maximum: 4
    """

    def mod_value(self, value: Any) -> int:
        """
        makes _RangeCheck compare the array length

        """
        return len(value)


class DateTimeRangeCheck(RangeCheck):
    """
    ensures that a 'sized' value is within a defined range.

    >>> check = DateTimeRangeCheck(
    ...     min_value=datetime.datetime.fromisoformat("2000-01-01T00:00:00.000+00:00"),
    ...     max_value=datetime.datetime.fromisoformat("2002-01-01T00:00:00.000+00:00")
    ... )
    >>> check.validate(datetime.datetime.fromisoformat("2001-01-01T00:00:00.000+00:00"))

    >>> check.validate(datetime.datetime.fromisoformat("2003-01-01T00:00:00.000+00:00"))
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Range validation failed. value is '2003-01-01 00:00:00+00:00'. minimum: 2000-01-01 00:00:00+00:00 maximum: 2002-01-01 00:00:00+00:00
    >>> check.validate(datetime.datetime.fromisoformat("1999-01-01T00:00:00.000+00:00"))
    Traceback (most recent call last):
        ...
    jason.schema.PropertyValidationError: Range validation failed. value is '1999-01-01 00:00:00+00:00'. minimum: 2000-01-01 00:00:00+00:00 maximum: 2002-01-01 00:00:00+00:00
    """

    def mod_param(
        self, param: Union[datetime.datetime, datetime.date]
    ) -> Union[datetime.datetime, datetime.date]:
        """
        if no timezone is provided, assume UTC

        """
        if param.tzinfo is None:
            param = param.replace(tzinfo=datetime.timezone.utc)
        return param
