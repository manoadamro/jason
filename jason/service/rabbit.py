from typing import Iterable

from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from ..config.flask import FlaskConfigMixin
from .base import Service


class RabbitService(Service):
    """
    Base class for rabbit consumer services

    """

    def __init__(self, config: FlaskConfigMixin, sidekicks: Iterable["Service"] = ()):
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
            **kwargs
        )

    def create_connection(self):
        """
        creates a rabbitmq blocking connection

        """
        return BlockingConnection(self.connection_parameters)
