from jason.core.configuration import props


class PostgresConfigMixin:
    DB_DRIVER = props.String(default="postgresql")
    DB_HOST = props.String()
    DB_PORT = props.String()
    DB_USER = props.String(nullable=True)
    DB_PASS = props.String(nullable=True)
    TEST_DB_URL = props.String(default="sqlite:///:memory:")
