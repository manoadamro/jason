import functools
import inspect
from typing import Any, Callable, Dict, Optional, Type

from flask import request

from jason.props import base, error, types, utils

from ..error import BatchValidationError
from ..exception import BadRequest


class RequestSchema:
    def __init__(
        self,
        model: Type[types.Model] = None,
        args: types.Model = None,
        json: types.Model = None,
        query: types.Model = None,
        form: types.Model = None,
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
    def from_model(model: Type[types.Model], name: str, default: Any = None) -> Any:
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
        if self.json is False:
            if request.is_json is True:
                raise error.RequestValidationError(
                    "request should not contain a json body"
                )
            return None
        if utils.is_instance_or_type(self.json, base.SchemaAttribute):
            return self.json.load(request.json)
        return request.json

    def __call__(self, func: Callable) -> Callable:
        func_info = inspect.signature(func)
        func_params = func_info.parameters

        @functools.wraps(func)
        def call(**kwargs: Any) -> Any:
            for name, value in self.load_view_args().items():
                kwargs[name] = value
            try:
                kwargs = self.load(
                    kwargs,
                    func_params,
                    json=self.load_json,
                    query=self.load_query,
                    form=self.load_form,
                )
            except BatchValidationError as ex:
                raise BadRequest(ex.message)
            return func(**kwargs)

        return call
