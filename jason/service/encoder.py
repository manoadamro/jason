from datetime import date, datetime

import flask.json


class JSONEncoder(flask.json.JSONEncoder):
    _object_encoders = {}
    _auto_encoders = {}

    def __init__(self, *args, **kwargs):
        super(JSONEncoder, self).__init__(*args, **kwargs)

    @staticmethod
    def _auto_encode(obj, fields=None):
        def _resolve(k, i):
            return k[i] if isinstance(k, (list, tuple)) else k

        field_map = {_resolve(k, 0): _resolve(k, 1) for k in fields} if fields else None

        def field_filter(field):
            return field.startswith("_") is False and (
                field_map is None or field in field_map
            )

        return {
            field_map[key] if field_map else key: getattr(obj, key)
            for key in dir(obj)
            if field_filter(key)
        }

    @classmethod
    def encode_object(cls, object_type):
        def _call(func):
            cls._object_encoders[object_type] = func
            return func

        return _call

    @classmethod
    def encode_all(cls, typ):
        if not isinstance(typ, type):
            raise TypeError(
                "JSONEncoder.auto should only be used to decorate class definitions"
            )
        cls._auto_encoders[typ] = None
        return typ

    @classmethod
    def encode_fields(cls, *field_names):
        def _call(typ):
            if not isinstance(typ, type):
                raise TypeError(
                    "JSONEncoder.auto should only be used to decorate class definitions"
                )
            cls._auto_encoders[typ] = field_names
            return typ

        return _call

    @classmethod
    def encode(cls, o, *fields):
        if fields:
            o = cls._auto_encode(o, fields)
        return super(JSONEncoder, cls()).encode(o)

    def default(self, obj):
        obj_type = type(obj)
        if obj_type in self._object_encoders:
            return self._object_encoders[obj_type](obj)
        if obj_type in self._auto_encoders:
            return self._auto_encode(obj, self._auto_encoders[obj_type])
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        return super(JSONEncoder, self).default(obj)
