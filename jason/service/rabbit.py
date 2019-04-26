from typing import Iterable, Type

from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from .base import Config as _Config
from .base import Service, props


class RabbitConfigMixin:
    RABBIT_HOST = props.String(default="localhost")
    RABBIT_PORT = props.Int(default=1234)  # TODO
    RABBIT_USER = props.String(default="guest")
    RABBIT_PASS = props.String(default="guest")


class Config(RabbitConfigMixin, _Config):
    ...


class RabbitService(Service):
    """
    Base class for rabbit consumer services

    """

    def __init__(self, config: Type[Config], sidekicks: Iterable["Service"] = ()):
        super(RabbitService, self).__init__(config=config, sidekicks=sidekicks)
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
        return BlockingConnection(self.connection_parameters)
