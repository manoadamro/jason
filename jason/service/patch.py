import flask


class FlaskMeta(type):
    @classmethod
    def __instancecheck__(mcs, instance):
        return type(instance).__name__ in ("App", "Service")


class MonkeyFlask(flask.Flask, metaclass=FlaskMeta):
    ...


flask.Flask = MonkeyFlask
