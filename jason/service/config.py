from typing import Type

from .. import props
from . import mixins


class ServiceConfig(props.ConfigObject):
    SERVE = props.Bool(default=True)
    TESTING = props.Bool(default=False)
    SERVE_HOST = props.String(default="localhost")
    SERVE_PORT = props.Int(default=5000)


_CONFIG_MIXIN_MAP = {
    "redis": mixins.RedisConfigMixin,
    "rabbit": mixins.RabbitConfigMixin,
    "postgres": mixins.PostgresConfigMixin,
    "celery": mixins.CeleryConfigMixin,
}


def _resolve_mixin(name, types):
    if name not in _CONFIG_MIXIN_MAP:
        raise KeyError(
            f"can not add config mix in for '{name}'. "
            f"valid mix ins are: {', '.join(_CONFIG_MIXIN_MAP.keys())}"
        )
    mixin = _CONFIG_MIXIN_MAP[name]
    if mixin in types:
        raise ValueError(f"Mixin '{mixin}' has already been added to config")
    return mixin


def make_config(*configs, **fields):
    types = []
    base = None
    for obj in configs:
        if isinstance(obj, type):
            if obj == ServiceConfig or issubclass(obj, ServiceConfig):
                if base is not None:
                    raise ValueError(
                        "Only one instance of 'ServiceConfig' can be passed to make_config"
                    )
                base = obj
            else:
                types.append(obj)
        elif isinstance(obj, str):
            mixin = _resolve_mixin(obj, types)
            types.append(mixin)
        else:
            raise ValueError(
                f"make_config only accepts string mixin names, mixin types or 'ServiceConfig'"
            )
    if base is None:
        base = ServiceConfig
    types.append(base)
    return type(
        "Config", tuple(types), {key.upper(): value for key, value in fields.items()}
    )
