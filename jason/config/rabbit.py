from jason.core.configuration import props


class RabbitConfigMixin:
    RABBIT_HOST = props.String(default="localhost")
    RABBIT_PORT = props.Int(default=1234)  # TODO
    RABBIT_USER = props.String(default="guest")
    RABBIT_PASS = props.String(default="guest")
