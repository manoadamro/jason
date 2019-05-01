from typing import Type

from .app import App
from .config import ServiceConfig
from .mixins import (
    CeleryConfigMixin,
    PostgresConfigMixin,
    RabbitConfigMixin,
    RedisConfigMixin,
)
from .service import Service
from .threads import AppThreads

service = Service


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
        types.append(RedisConfigMixin)
    if rabbit:
        types.append(RabbitConfigMixin)
    if postgres:
        types.append(PostgresConfigMixin)
    if celery:
        types.append(CeleryConfigMixin)
    types.append(base or ServiceConfig)
    return type("Config", tuple(types), fields or {})
