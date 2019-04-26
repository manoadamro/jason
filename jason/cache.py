import redis

from jason.configuration import props


class RedisConfigMixin:
    REDIS_HOST = props.String()
    REDIS_PORT = props.Int()
    REDIS_PASS = props.String()


Cache = redis.StrictRedis
