from typing import Iterable, Type

from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from .base import Config as _Config
from .base import Service, props


class RabbitConfigMixin:
    RABBIT_HOST = props.String(default="localhost")
    RABBIT_PORT = props.Int(default=5672)
    RABBIT_USER = props.String(default="guest")
    RABBIT_PASS = props.String(default="guest")


class Config(RabbitConfigMixin, _Config):
    ...


class RabbitService(Service):
    """
    Base class for rabbit consumer services

    """

    def __init__(
        self,
        name: str,
        config: Type[Config],
        sidekicks: Iterable["Service"] = (),
        testing: bool = False,
        **kwargs,
    ):
        super(RabbitService, self).__init__(
            name=name, config=config, sidekicks=sidekicks, testing=testing, **kwargs
        )
        self.connection = None
        self.channel = None

    @property
    def credentials(self):
        """
        rabbitmq connection credentials

        """
        return PlainCredentials(
            username=self.config.RABBIT_USER, password=self.config.RABBIT_PASS
        )

    @property
    def connection_parameters(self, **kwargs):
        """
        rabbitmq connection parameters

        """
        return ConnectionParameters(
            host=self.config.RABBIT_HOST,
            port=self.config.RABBIT_PORT,
            credentials=self.credentials,
            **kwargs,
        )

    def create_connection(self):
        """
        creates a rabbitmq blocking connection

        """
        self.logger.info("creating rabbit connection for service %s", self.name)
        return BlockingConnection(self.connection_parameters)
