from typing import Type as _Type

from . import crypto, props
from .service import AppThreads
from .service import RequestSchema as _RequestSchema
from .service import Service, ServiceConfig, mixins
from .token import Protect as _Protect
from .token import TokenHandler, TokenValidationError

token_protect = _Protect
request_schema = _RequestSchema
service = Service


def make_config(
    base: _Type[ServiceConfig] = None,
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
