from datetime import date, datetime

import flask.json


class JSONEncoder(flask.json.JSONEncoder):
    _object_encoders = {}
    _auto_encoders = []

    def __init__(self, *args, **kwargs):
        super(JSONEncoder, self).__init__(*args, **kwargs)

    @classmethod
    def object(cls, object_type):
        def _call(func):
            cls._object_encoders[object_type] = func

        return _call

    @classmethod
    def auto(cls, typ):
        if not isinstance(typ, type):
            raise TypeError(
                "JSONEncoder.auto should only be used to decorate class definitions"
            )
        cls._auto_encoders.append(typ)
        return typ

    @staticmethod
    def _auto_encode(obj):
        return {key: getattr(obj, key) for key in dir(obj) if not key.startswith("_")}

    def default(self, obj):
        obj_type = type(obj)
        if obj_type in self._object_encoders:
            return self._object_encoders[obj_type](obj)
        if obj_type in self._auto_encoders:
            return self._auto_encode(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        return super(JSONEncoder, self).default(obj)
