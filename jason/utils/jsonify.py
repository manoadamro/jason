import flask

_jsonify = flask.jsonify


def jsonify(obj, key=None, **kwargs):
    def _get(item, key):
        if isinstance(item, dict):
            return item[key]
        return getattr(item, key)

    if isinstance(obj, (list, tuple)):
        if key is not None:
            obj = {_get(item, key): item for item in obj}
    elif key is not None:
        raise ValueError("key provided for jsonification but object is not iterable")
    return _jsonify(obj, **kwargs)


flask.jsonify = jsonify
