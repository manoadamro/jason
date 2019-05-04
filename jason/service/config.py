from typing import Type

from . import mixins
from .. import props


class ServiceConfig(props.ConfigObject):
    SERVE = props.Bool(default=True)
    SERVE_HOST = props.String(default="localhost")
    SERVE_PORT = props.Int(default=5000)


_CONFIG_MIXIN_MAP = {
    "redis": mixins.RedisConfigMixin,
    "rabbit": mixins.RabbitConfigMixin,
    "postgres": mixins.PostgresConfigMixin,
    "celery": mixins.CeleryConfigMixin,
}


def make_config(*configs, base: Type[ServiceConfig] = None, **fields):
    types = []
    for name in configs:
        if name not in _CONFIG_MIXIN_MAP:
            raise KeyError(
                f"can not add config mix in for '{name}'. "
                f"valid mix ins are: {', '.join(_CONFIG_MIXIN_MAP.keys())}"
            )
        types.append(_CONFIG_MIXIN_MAP[name])
    types.append(base or ServiceConfig)
    return type("Config", tuple(types), fields or {})
