# TODO break up

import datetime
import functools
import inspect
import os
import re
import uuid
from typing import Any, Callable, Dict, List, Optional, Pattern, Tuple, Type, Union

from flask import request

from . import base, error, range, utils


class AnyOf(base.SchemaAttribute):
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


class Property(base.SchemaAttribute):
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
        if value is None:
            value = utils.maybe_call(value=self.default)
        if value is None:
            if not self.nullable:
                raise error.PropertyValidationError(f"Property is not nullable")
            return None
        if self.types and (
            (utils.is_bool(value) and bool not in self.types)
            or not isinstance(value, self.types)
        ):
            raise error.PropertyValidationError(
                f"Property was expected to be of type: "
                f"{', '.join(t.__name__ for t in self.types)}. not {type(value).__name__}"
            )
        return self._validate(value)

    def _validate(self, value: Any) -> Any:
        return value

    def __call__(self, func: Callable[[Any], Any]) -> "Property":
        base_validator = self._validate

        def wrapped_validator(value: Any) -> Any:
            value = base_validator(value)
            return func(value)

        self._validate = wrapped_validator
        return self


class Choice(Property):
    def __init__(
        self, choices: List = None, nullable: bool = False, default: Any = None
    ):
        super(Choice, self).__init__(nullable=nullable, default=default)
        self.choices = choices

    def _validate(self, value: Any) -> Any:
        if self.choices and value not in self.choices:
            raise error.PropertyValidationError(
                f"Property was expected to be one of: {', '.join((str(c) for c in self.choices))}"
            )
        return value


class Model:
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
    def __init__(
        self,
        prop: Union[base.SchemaAttribute, Type[base.SchemaAttribute]],
        min_length: Union[int, Callable[[], int]] = None,
        max_length: Union[int, Callable[[], int]] = None,
        **kwargs: Any,
    ):
        if isinstance(prop, type):
            prop = prop()
        super(Array, self).__init__(types=(list, tuple), **kwargs)
        self.range = range.SizeRangeCheck(min_value=min_length, max_value=max_length)
        self.prop = prop

    def _validate(self, value: Union[List, Tuple]) -> Union[List, Tuple]:

        self.range.validate(value)
        errors = []
        validated = []
        for item in value:
            try:
                value = self.prop.load(item)
            except error.PropertyValidationError as ex:
                errors.append(f"could not validate {value}: {ex}")
                continue
            validated.append(value)
        if errors:
            raise error.BatchValidationError(
                f"failed to validate {value} against {self}", errors
            )
        return validated


class Nested(Property):
    def __init__(
        self, model: Union[Type[Model], Model], strict: bool = None, **kwargs: Any
    ):
        super(Nested, self).__init__(types=(dict,), **kwargs)
        self.props = model.__props__
        if strict is None:
            strict = getattr(model, "__strict__")
        self.strict = strict

    def _validate(self, obj: Dict[Any, Any]) -> Dict[Any, Any]:

        validated = {}
        errors = []
        for field, prop in self.props.items():
            value = obj.get(field, None)
            try:
                validated[field] = prop.load(value)
            except error.PropertyValidationError as ex:
                errors.append(f"could not load property '{field}': {ex}")
                continue
        if self.strict:
            extras = [k for k in obj if k not in self.props]
            if len(extras):
                errors.append(
                    f"Strict mode is True and supplied object contains extra keys: "
                    f"'{', '.join(extras)}'"
                )
        if errors:
            raise error.BatchValidationError(
                f"failed to validate {obj} against {self}", errors
            )
        return validated


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


class Combine(Inline):
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
        super(Combine, self).__init__(props=schema, **kwargs)


class Bool(Property):
    def __init__(self, allow_strings: bool = True, **kwargs: Any):
        super(Bool, self).__init__(types=(str, bool), **kwargs)
        self.allow_strings = allow_strings

    def _from_string(self, value: str) -> bool:

        if not self.allow_strings:
            raise error.PropertyValidationError(
                "Loading boolean from string is not allowed"
            )
        value = value.lower()
        if value == "true":
            value = True
        elif value == "false":
            value = False
        else:
            raise error.PropertyValidationError(
                f"Could not coerce string '{value}' to boolean"
            )
        return value

    def _validate(self, value: Union[str, bool]) -> bool:

        if isinstance(value, str):
            value = self._from_string(value)
        return value


class Number(Property):
    def __init__(
        self,
        min_value: Union[Callable[[], int], int] = None,
        max_value: Union[Callable[[], int], int] = None,
        allow_strings: bool = True,
        types: Tuple[Type, ...] = (int, float, str),
        **kwargs: Any,
    ):
        super(Number, self).__init__(types=types, **kwargs)
        self.range = range.RangeCheck(min_value=min_value, max_value=max_value)
        self.allow_strings = allow_strings

    def _from_string(self, value: str) -> Union[int, float]:
        if not self.allow_strings:
            raise error.PropertyValidationError(
                "Loading number from string is not allowed"
            )
        if "." in value and value.replace(".", "", 1).isnumeric():
            value = float(value)
        elif value.isnumeric():
            value = int(value)
        else:
            raise error.PropertyValidationError(
                f"Could not coerce string '{value}' to number"
            )
        return value

    def _validate(self, value: Union[int, float, str]) -> Union[int, float]:
        if isinstance(value, str):
            value = self._from_string(value)
        self.range.validate(value)
        return value


class Int(Number):
    def __init__(self, **kwargs: Any):
        super(Int, self).__init__(types=(str, int), **kwargs)

    def _validate(self, value: Union[int, str]) -> int:
        return super(Int, self)._validate(value)


class Float(Number):
    def __init__(self, **kwargs: Any):
        super(Float, self).__init__(types=(str, int, float), **kwargs)

    def _validate(self, value: Union[int, float, str]) -> float:
        value = super(Float, self)._validate(value)
        return float(value)


class String(Property):
    def __init__(
        self,
        min_length: Union[Callable[[], int], int] = None,
        max_length: Union[Callable[[], int], int] = None,
        **kwargs: Any,
    ):
        super(String, self).__init__(types=(str,), **kwargs)
        self.range = range.SizeRangeCheck(min_value=min_length, max_value=max_length)

    def _validate(self, value: str) -> str:
        self.range.validate(value)
        return value


class Regex(String):
    def __init__(self, matcher: Union[str, Pattern], **kwargs: Any):
        super(Regex, self).__init__(**kwargs)
        if isinstance(matcher, str):
            matcher = re.compile(matcher)
        self.matcher = matcher

    def _validate(self, value: str) -> str:
        if re.match(self.matcher, value) is None:
            raise error.PropertyValidationError(
                f"String value '{value}' did not match regex pattern '{self.matcher.pattern}'"
            )
        return value


class Uuid(String):
    def __init__(self):
        super(Uuid, self).__init__()

    def _validate(self, value: str) -> str:

        try:
            uuid.UUID(value)
        except ValueError:
            raise error.PropertyValidationError(f"value '{value}' is not a valid uuid")
        return value


class Date(Property):
    def __init__(
        self,
        min_value: Union[Callable[[], int], int] = None,
        max_value: Union[Callable[[], int], int] = None,
        allow_strings: bool = True,
        **kwargs: Any,
    ):
        super(Date, self).__init__(types=(datetime.date, str), **kwargs)
        self.range = range.RangeCheck(min_value=min_value, max_value=max_value)
        self.allow_strings = allow_strings

    def _from_string(self, value: str) -> datetime.date:

        if not self.allow_strings:
            raise error.PropertyValidationError(
                "Loading date from string is not allowed"
            )
        try:
            value = datetime.date.fromisoformat(value)
        except ValueError:
            raise error.PropertyValidationError(
                f"Could not coerce string '{value}' to date object"
            )
        return value

    def _validate(self, value: Union[str, datetime.date]) -> datetime.date:
        if isinstance(value, str):
            value = self._from_string(value)
        self.range.validate(value)
        return value


class Datetime(Property):
    def __init__(
        self,
        min_value: Union[Callable[[], int], int] = None,
        max_value: Union[Callable[[], int], int] = None,
        allow_strings: bool = True,
        **kwargs: Any,
    ):
        super(Datetime, self).__init__(types=(datetime.datetime, str), **kwargs)
        self.range = range.DateTimeRangeCheck(min_value=min_value, max_value=max_value)
        self.allow_strings = allow_strings

    def _from_string(self, value: str) -> datetime.datetime:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        if not self.allow_strings:
            raise error.PropertyValidationError(
                "Loading datetime from string is not allowed"
            )
        try:
            value = datetime.datetime.fromisoformat(value)
        except ValueError:
            raise error.PropertyValidationError(
                f"Could not coerce string '{value}' to datetime object"
            )
        return value

    def _validate(self, value: Union[datetime.datetime, str]) -> datetime.datetime:
        if isinstance(value, str):
            value = self._from_string(value)
        if value.tzinfo is None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        self.range.validate(value)
        return value


class Password(String):

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

        score = 0
        if re.search(self.whitespace_matcher, value):
            raise error.PropertyValidationError(
                f"Password must not contain white space"
            )

        if re.search(self.uppercase_matcher, value):
            if self.uppercase is False:
                raise error.PropertyValidationError(
                    f"Password must not contain uppercase characters"
                )
            score += 1
        elif self.uppercase is True:
            raise error.PropertyValidationError(
                f"Password must contain at least 1 uppercase character"
            )

        if re.search(self.numbers_matcher, value):
            if self.numbers is False:
                raise error.PropertyValidationError(
                    f"Password must not contain numbers"
                )
            score += 1
        elif self.numbers is True:
            raise error.PropertyValidationError(
                f"Password must contain at least 1 number"
            )

        if re.search(self.symbols_matcher, value):
            if self.symbols is False:
                raise error.PropertyValidationError(
                    f"Password must not contain symbol characters"
                )
            score += 1
        elif self.symbols is True:
            raise error.PropertyValidationError(
                f"Password must contain at least 1 symbol character"
            )

        if score < self.min_score:
            raise error.PropertyValidationError(
                f"Password is too weak. "
                f"minimum score: {self.min_score}. "
                f"current score: {score}"
            )

        return value


class Email(Regex):
    matcher = re.compile("^[^@]+@[^@]+\\.[^@]+$")

    def __init__(self, **kwargs: Any):
        super(Email, self).__init__(self.matcher, **kwargs)


class RequestSchema:
    def __init__(
        self,
        model: Type[Model] = None,
        args: Model = None,
        json: Model = None,
        query: Model = None,
        form: Model = None,
    ):
        self.args = (
            args if args is not None else self.from_model(model, "Args", default=False)
        )
        self.json = (
            json if json is not None else self.from_model(model, "Json", default=False)
        )
        self.query = (
            query
            if query is not None
            else self.from_model(model, "Query", default=False)
        )
        self.form = (
            form if form is not None else self.from_model(model, "Form", default=False)
        )

    @staticmethod
    def load(
        kwargs: Dict[str, Any],
        func_params: Dict[str, Any],
        **funcs: Callable[[], Dict[str, Any]],
    ) -> Dict[str, Any]:
        errors = []
        for name, func in funcs.items():
            try:
                data = func()
                if name in func_params:
                    kwargs[name] = data
            except (error.PropertyValidationError, error.BatchValidationError) as ex:
                errors.append(f"failed to load {name}: {ex}")
        if errors:
            raise error.BatchValidationError("failed to validate request", errors)
        return kwargs

    @staticmethod
    def from_model(model: Type[Model], name: str, default: Any = None) -> Any:
        if model is None:
            return None
        if hasattr(model, name):
            return getattr(model, name)
        upper = name.upper()
        if hasattr(model, upper):
            return getattr(model, upper)
        lower = name.lower()
        if hasattr(model, lower):
            return getattr(model, lower)
        return default

    def load_view_args(self) -> Optional[Dict[str, Any]]:
        args = request.view_args or {}
        if utils.is_instance_or_type(self.args, base.SchemaAttribute):
            return self.args.load(args)
        return args

    def load_query(self) -> Optional[Dict[str, Any]]:
        query = request.args
        if utils.is_instance_or_type(self.query, base.SchemaAttribute):
            return self.query.load(query)
        return query

    def load_form(self) -> Optional[Dict[str, Any]]:
        if self.form is True:
            if request.form is None:
                raise error.RequestValidationError("request requires a form")
            return request.form
        if self.form is False:
            if request.form is not None:
                raise error.RequestValidationError("request should not contain a form")
            return None
        if utils.is_instance_or_type(self.form, base.SchemaAttribute):
            return self.form.load(request.form)
        return request.form

    def load_json(self) -> Optional[Dict[str, Any]]:
        if self.json is True:
            if request.is_json is False:
                raise error.RequestValidationError("request requires a json body")
            return request.json
        elif self.json is False:
            if request.is_json is True:
                raise error.RequestValidationError(
                    "request should not contain a json body"
                )
            return None
        elif utils.is_instance_or_type(self.json, base.SchemaAttribute):
            return self.json.load(request.json)
        return request.json

    def __call__(self, func: Callable) -> Callable:
        func_info = inspect.signature(func)
        func_params = func_info.parameters

        @functools.wraps(func)
        def call(**kwargs: Any) -> Any:
            for name, value in self.load_view_args().items():
                kwargs[name] = value
            kwargs = self.load(
                kwargs,
                func_params,
                json=self.load_json,
                query=self.load_query,
                form=self.load_form,
            )
            return func(**kwargs)

        return call


class Config(Model):
    @classmethod
    def load(cls, **fields: Any) -> "Config":
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
            return super(Config, self).__getattribute__(item)
        except AttributeError:
            return getattr(self.__dict__, item)

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__dict__[key] = value
