from datetime import date, datetime

import flask.json


class JSONEncoder(flask.json.JSONEncoder):
    _object_encoders = {}

    def __init__(self):
        super(JSONEncoder, self).__init__()

    @classmethod
    def object(cls, object_type):
        def _call(func):
            cls._object_encoders[object_type] = func

        return _call

    def default(self, obj):
        obj_type = type(obj)
        if obj_type in self._object_encoders:
            return self._object_encoders[obj_type](obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        return super(JSONEncoder, self).default(obj)
