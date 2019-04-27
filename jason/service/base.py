import logging
from typing import Any, Type

from jason.config import Config, props

from ..cache import RedisConfigMixin, redis_cache
from ..database import PostgresConfigMixin, Session, postgres_engine

Config = Config
props = props


class Service:
    """
    Base class for all services.

    """

    def __init__(
        self,
        name: str,
        config: Type[Config],
        testing: bool = False,
        use_db: bool = False,
        use_cache: bool = False,
        **kwargs: Any,
    ):
        self.name = name
        self.testing = testing
        self.config = config.load(**kwargs)
        self.logger = logging.getLogger(self.name)

        if use_db:
            self.init_database()

        if use_cache:
            self.init_cache()

    def init_database(self):
        if not isinstance(self.config, PostgresConfigMixin):
            raise ValueError(
                f"can not init database with config. "
                f"config must be sub class of PostgresConfigMixin"
            )
        engine = postgres_engine(self.config, testing=self.testing)
        Session.configure(bind=engine)

    def init_cache(self, **kwargs: Any):
        if not isinstance(self.config, RedisConfigMixin):
            raise ValueError(
                f"can not init database with config. "
                f"config must be sub class of RedisConfigMixin"
            )
        redis_cache.init(self.config, **kwargs)

    def start(self):
        """
        starts and runs the service.

        """
        self.logger.info("starting service %s", self.name)
        self.set_up()
        try:
            self.main()
        except Exception as ex:
            self.logger.exception("service error on %s", self.name, exc_info=ex)
            self.on_error(ex)
            raise
        else:
            self.logger.info("tearing down service %s", self.name)
            self.tear_down()
        finally:
            self.logger.info("closing service %s", self.name)
            self.on_close()
        self.logger.info("closed service %s", self.name)

    def set_up(self):
        """
        called before `main` method

        """
        ...

    def main(self):
        """
        the main service method

        """
        ...

    def tear_down(self):
        """
        called when main method exits,
        assuming there were no errors

        """
        ...

    def on_error(self, ex):
        """
        called when main method exits due to an error

        """
        ...

    def on_close(self):
        """
        called before process exits,
        regardless of errors

        """
        ...
