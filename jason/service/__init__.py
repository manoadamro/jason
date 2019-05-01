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


def make_config(
    base, redis=False, rabbit=False, postgres=False, celery=False, fields=None
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
    types.append(base)
    return type("Config", tuple(types), fields or {})
