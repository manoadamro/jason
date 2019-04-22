import sqlalchemy
import sqlalchemy.orm

from jason.core.configuration import props


class PostgresConfigMixin:
    DB_DRIVER = props.String(default="postgresql")
    DB_HOST = props.String()
    DB_PORT = props.String()
    DB_USER = props.String(nullable=True)
    DB_PASS = props.String(nullable=True)
    TEST_DB_URL = props.String(default="sqlite:///:memory:")


def scoped_session(factory):
    return sqlalchemy.orm.scoped_session(factory)


def postgres_engine(config: PostgresConfigMixin, testing=False):
    if not testing:
        if config.DB_USER:
            credentials = f"{config.DB_USER}:{config.DB_PASS}@"
        else:
            credentials = ""
        host = f"{config.DB_HOST}:{config.DB_PORT}"
        db_url = f"{config.DB_DRIVER}://{credentials}{host}"
    else:
        db_url = config.TEST_DB_URL
    return sqlalchemy.create_engine(db_url, echo=True)
