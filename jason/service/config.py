from jason import props


class ServiceConfig(props.Config):
    SERVE = props.Bool(default=True)
    SERVE_HOST = props.String(default="localhost")
    SERVE_PORT = props.Int(default=5000)