"""
api.schema

"""
import functools
import inspect
from typing import Any, Callable, Dict, Optional, Type

from flask import request

from .. import schema, utils

props = schema


class RequestValidationError(props.PropertyValidationError):
    """
    raised when `RequestSchema` to validate a request

    """

    ...


class RequestSchema:
    """
    Validates a flask requests content.

    validatable objects:
    - args: parts of the url, eg. /thing/<thing_id>
    - query: the url query, eg. ?thing=123
    - json: the json body
    - form: the form body

    request schemas can be defined in a number of ways.
    you can define a class with nested models or object type properties (eg Inline, Nested, etc):

    >>> class MyRequestSchema:
    ...
    ...     class Args(schema.Model):
    ...         q = schema.String(default="something")
    ...         i = schema.Int(nullable=True)
    ...
    ...     json = schema.Inline(props={"q": schema.String(default="something")})
    ...
    >>> @request_schema(model=RequestSchema)
    ... def some_route(q, json):
    ...     ...

    or you can define them inline:

    >>> @request_schema(
    ...     args=schema.Nested(MyRequestSchema.Args),
    ...     json=schema.Inline(props={"q": schema.String(default="something")})
    ... )
    ... def some_route(q, json):
    ...     ...

    the decorated method will work like pytest fixtures
    in the way that you can have validatable elements passed to it, regardless of validation rules.
    simply by adding it to the signature.

    NOTE: view_args (args) will not be packaged as a dict but passed individually.

    example:

    >>> @request_schema(
    ...     args=schema.Nested(MyRequestSchema.Args),
    ...     json=schema.Inline(props={"something": schema.String(default="hello")})
    ... )
    ... def some_route(q, i, json):
    ...     ...


    >>> @request_schema(
    ...     args=schema.Nested(MyRequestSchema.Args),
    ...     json=schema.Inline(props={"something": schema.String(default="hello")})
    ... )
    ... def some_route(q, i, json):  # this will receive the url args and json
    ...     ...

    >>> @request_schema(
    ...     args=schema.Nested(MyRequestSchema.Args),
    ...     json=schema.Inline(props={"something": schema.String(default="hello")})
    ... )
    ... def some_route(json):  # this will receive only the json
    ...     ...

    >>> @request_schema(
    ...     args=schema.Nested(MyRequestSchema.Args),
    ...     json=schema.Inline(props={"something": schema.String(default="hello")})
    ... )
    ... def some_route(q, i, query, form, json):  # this will receive everything (form and query will be un-validated)
    ...     ...

    """

    def __init__(
        self,
        model: Type[props.Model] = None,
        args: props.Model = None,
        json: props.Model = None,
        query: props.Model = None,
        form: props.Model = None,
    ):
        self.args = args if args is not None else self.from_model(model, "Args")
        self.json = json if json is not None else self.from_model(model, "Json")
        self.query = query if query is not None else self.from_model(model, "Query")
        self.form = form if form is not None else self.from_model(model, "Form")

    @staticmethod
    def load(
        kwargs: Dict[str, Any],
        func_params: Dict[str, Any],
        **funcs: Callable[[], Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        generates kwargs to call decorated method with based on 'func_params' and a validator map 'funcs'

        """
        for name, func in funcs.items():
            data = func()
            if name in func_params:
                kwargs[name] = data
        return kwargs

    @staticmethod
    def from_model(model: Type[props.Model], name: str) -> Any:
        """
        attempts to load rules from a model that has been passed into constructed as 'model'

        """
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
        return None

    def load_view_args(self) -> Optional[Dict[str, Any]]:
        """
        loads the view args (args) from flask request, validates and returns

        """
        args = request.view_args or {}
        if utils.is_instance_or_type(self.args, props.SchemaAttribute):
            return self.args.load(args)
        return args

    def load_query(self) -> Optional[Dict[str, Any]]:
        """
        loads the args (query) from flask request, validates and returns

        """
        query = request.args
        if utils.is_instance_or_type(self.query, props.SchemaAttribute):
            return self.query.load(query)
        return query

    def load_form(self) -> Optional[Dict[str, Any]]:
        """
        loads the form from flask request, validates and returns

        """
        if self.form is True:
            if request.form is None:
                raise RequestValidationError  # TODO
            return request.form
        if self.form is False:
            if request.form is not None:
                raise RequestValidationError  # TODO
            return None
        if utils.is_instance_or_type(self.form, props.SchemaAttribute):
            return self.form.load(request.form)
        return request.form

    def load_json(self) -> Optional[Dict[str, Any]]:
        """
        loads the json from flask request, validates and returns

        """
        if self.json is True:
            if request.is_json is False:
                raise RequestValidationError  # TODO
            return request.json
        elif self.json is False:
            if request.is_json is True:
                raise RequestValidationError  # TODO
            return None
        elif utils.is_instance_or_type(self.json, props.SchemaAttribute):
            return self.json.load(request.json)
        return request.json

    def __call__(self, func: Callable) -> Callable:
        """
        decorator method, inspects the decorated function to determine which kwargs to pass.
        view args (args) are mandatory.

        """
        func_info = inspect.signature(func)
        func_params = func_info.parameters

        @functools.wraps(func)
        def call(**kwargs: Any) -> Any:
            """
            loads and validates the current request based on the defined rules.

            """
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


request_schema = RequestSchema
