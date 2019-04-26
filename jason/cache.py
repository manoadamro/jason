import redis

from jason.config import props


class RedisConfigMixin:
    REDIS_HOST = props.String()
    REDIS_PORT = props.Int()
    REDIS_PASS = props.String()


class Cache:
    def __init__(self):
        self._cache = None

    def init(self, config: RedisConfigMixin, **kwargs):
        self._cache = redis.StrictRedis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            password=config.REDIS_PASS,
            **kwargs
        )

    def get(self, name):
        if not self._cache:
            raise RuntimeError  # TODO
        return self._cache.get(name)

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        if not self._cache:
            raise RuntimeError  # TODO
        self._cache.set(name, value, ex=ex, px=px, nx=nx, xx=xx)
