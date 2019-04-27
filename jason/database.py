import sqlalchemy.orm
from sqlalchemy.ext import declarative

from jason.config import props

db = sqlalchemy
orm = sqlalchemy.orm
model_factory = sqlalchemy.ext.declarative.declarative_base
Session = sqlalchemy.orm.sessionmaker()


def scoped_session():
    return sqlalchemy.orm.scoped_session(Session)


class PostgresConfigMixin:
    DB_DRIVER = props.String(default="postgresql")
    DB_HOST = props.String()
    DB_PORT = props.String()
    DB_USER = props.String(nullable=True)
    DB_PASS = props.String(nullable=True)
    TEST_DB_URL = props.String(default="sqlite:///:memory:")


def postgres_engine(config: PostgresConfigMixin, testing=False):
    """
    builds a connection uri based on config options and returns an engine.

    NOTE: if testing is true, the uri will be to an in-memory sqlite database

    """
    if not testing:
        if config.DB_USER:
            credentials = f"{config.DB_USER}:{config.DB_PASS}@"
        else:
            credentials = ""
        host = f"{config.DB_HOST}:{config.DB_PORT}"
        db_url = f"{config.DB_DRIVER}://{credentials}{host}"
    else:
        db_url = config.TEST_DB_URL
    return db.create_engine(db_url, echo=True)
