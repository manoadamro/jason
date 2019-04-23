import json

from jason.config.flask import FlaskConfigMixin
from jason.config.postgres import PostgresConfigMixin
from jason.config.rabbit import RabbitConfigMixin
from jason.service import Config, FlaskService, RabbitService, props

from .database import Log
from .management_api import blueprint as management_api_blueprint


class ServiceConfig(FlaskConfigMixin, PostgresConfigMixin, RabbitConfigMixin, Config):
    LOG_EXCHANGE = props.String(default="logs")
    LOG_QUEUE = props.String(default="log_queue")


class LoggingManagementApi(FlaskService):
    def set_up(self):
        self.app.register_blueprint(management_api_blueprint)

    def main(self):
        self.serve()


class LoggingService(RabbitService):
    prefetch_count = 1
    durable = True

    def set_up(self):
        self.connection = self.create_connection()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.config.LOG_EXCHANGE, durable=self.durable
        )
        self.channel.queue_declare(queue=self.config.LOG_QUEUE, durable=self.durable)
        self.channel.queue_bind(
            exchange=self.config.LOG_EXCHANGE, queue=self.config.LOG_QUEUE
        )
        self.channel.basic_qos(prefetch_count=self.prefetch_count)
        self.channel.basic_consume(
            queue=self.config.LOG_QUEUE, on_message_callback=self.on_message_received
        )

    def main(self):
        self.channel.start_consuming()

    def on_message_received(self, ch, method, _properties, body):
        db_session = self.db_handler()
        data = json.loads(body)
        log = Log(**data)
        db_session.add(log)
        db_session.commit()
        ch.basic_ack(delivery_tag=method.delivery_tag)
