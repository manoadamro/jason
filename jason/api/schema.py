import functools
import inspect

from flask import request

from .. import schema as _schema

props = _schema


class RequestSchema:
    def __init__(self, model=None, params=None, query=None, json=None, form=None):
        self.model = model
        self.params = params or self.get_sub_model("Params")
        self.query = query or self.get_sub_model("Query")
        self.json = json or self.get_sub_model("Json")
        self.form = form or self.get_sub_model("Form")

    @staticmethod
    def load_property_data(data, sub_model):
        if sub_model is not None:
            data = sub_model.load(data)
        else:
            data = data or {}
        return data

    def get_sub_model(self, name):
        if not self.model:
            return None
        upper = name.upper()
        if hasattr(self.model, upper):
            return getattr(self.model, upper)
        lower = name.lower()
        if hasattr(self.model, lower):
            return getattr(self.model, lower)
        return getattr(self.model, name, None)

    def __call__(self, func):
        func_info = inspect.signature(func)
        func_params = func_info.parameters

        @functools.wraps(func)
        def call(*args, **kwargs):

            # params
            params_data = self.load_property_data(request.view_args, self.params)
            for name, value in params_data.items():
                kwargs[name] = value

            # query
            query_data = self.load_property_data(request.args, self.query)
            if "query" in func_params:
                kwargs["query"] = query_data

            # json
            json_data = self.load_property_data(request.json, self.json)
            if "json" in func_params:
                kwargs["json"] = json_data

            # form
            form_data = self.load_property_data(request.form, self.form)
            if "form" in func_params:
                kwargs["form"] = form_data
            return func(*args, **kwargs)

        return call


request_schema = RequestSchema
