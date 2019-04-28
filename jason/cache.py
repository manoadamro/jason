import redis

from jason.config import Config, props

Config = Config
props = props


class RedisConfigMixin:
    REDIS_HOST = props.String()
    REDIS_PORT = props.Int()
    REDIS_PASS = props.String()


class RedisCache:
    def __init__(self, testing: bool = False):
        self._cache = None
        self.testing = testing

    def init(self, config: RedisConfigMixin, testing: bool = None, **kwargs):
        if testing is not None:
            self.testing = testing
        self._cache = redis.StrictRedis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            password=config.REDIS_PASS,
            **kwargs
        )

    def get(self, name):
        if not self._cache:
            raise RuntimeError("cache has not yet been initialised")
        return self._cache.get(name)

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        if not self._cache:
            raise RuntimeError("cache has not yet been initialised")
        self._cache.set(name, value, ex=ex, px=px, nx=nx, xx=xx)


redis_cache = RedisCache()
