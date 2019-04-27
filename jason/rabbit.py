from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from jason.config import Config, props

Config = Config
props = props


class RabbitConfigMixin:
    RABBIT_HOST = props.String(default="localhost")
    RABBIT_PORT = props.Int(default=5672)
    RABBIT_USER = props.String(default="guest")
    RABBIT_PASS = props.String(default="guest")


def create_connection(config, **kwargs):
    return BlockingConnection(
        ConnectionParameters(
            host=config.RABBIT_HOST,
            port=config.RABBIT_PORT,
            credentials=PlainCredentials(
                username=config.RABBIT_USER, password=config.RABBIT_PASS
            ),
            **kwargs,
        )
    )
