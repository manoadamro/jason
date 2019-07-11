from jason import mixins

try:
    import flask_redis
except (ImportError, ModuleNotFoundError):
    raise ImportError(
        "package 'flask_redis' is not installed.\nYou can install it with:\npip3 install flask_redis"
    )


class Redis(flask_redis.FlaskRedis):
    def init_app(self, app, **kwargs):
        app.assert_mixin(mixins.RedisConfigMixin, "cache")
        app.config.REDIS_URL = self._redis_uri()
        super(Redis, self).init_app(app=app, **kwargs)

    @staticmethod
    def _database_uri(config):
        if config.REDIS_PASS is not None:
            credentials = f":{config.REDIS_PASS}@"
        else:
            credentials = None
        uri = f"{config.REDIS_DRIVER}://{credentials}{config.REDIS_HOST}:{config.REDIS_PORT}"
        return uri
