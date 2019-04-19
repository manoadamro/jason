import functools
import inspect

from flask import request

from .. import schema, utils

props = schema


class RequestValidationError(props.PropertyValidationError):
    """
    raised when `RequestSchema` to validate a request

    """

    ...


class RequestSchema:
    def __init__(self, model=None, args=None, json=None, query=None, form=None):
        self.args = args if args is not None else self.from_model(model, "Args")
        self.json = json if json is not None else self.from_model(model, "Json")
        self.query = query if query is not None else self.from_model(model, "Query")
        self.form = form if form is not None else self.from_model(model, "Form")

    @staticmethod
    def load(kwargs, func_params, **funcs):
        for name, func in funcs.items():
            data = func()
            if name in func_params:
                kwargs[name] = data
        return kwargs

    @staticmethod
    def from_model(model, name):
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

    def load_view_args(self):
        args = request.view_args or {}
        if utils.is_instance_or_type(self.args, props.SchemaAttribute):
            return self.args.load(args)
        return args

    def load_query(self):
        query = request.args
        if utils.is_instance_or_type(self.query, props.SchemaAttribute):
            return self.query.load(query)
        return query

    def load_form(self):
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

    def load_json(self):
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

    def __call__(self, func):
        func_info = inspect.signature(func)
        func_params = func_info.parameters

        @functools.wraps(func)
        def call(**kwargs):
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
