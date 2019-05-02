from typing import Type

from . import mixins
from .. import props


class ServiceConfig(props.ConfigObject):
    SERVE = props.Bool(default=True)
    SERVE_HOST = props.String(default="localhost")
    SERVE_PORT = props.Int(default=5000)


def make_config(
    base: Type[ServiceConfig] = None,
    redis: bool = False,
    rabbit: bool = False,
    postgres: bool = False,
    celery: bool = False,
    fields: bool = None,
):
    types = []
    if redis:
        types.append(mixins.RedisConfigMixin)
    if rabbit:
        types.append(mixins.RabbitConfigMixin)
    if postgres:
        types.append(mixins.PostgresConfigMixin)
    if celery:
        types.append(mixins.CeleryConfigMixin)
    types.append(base or ServiceConfig)
    return type("Config", tuple(types), fields or {})
