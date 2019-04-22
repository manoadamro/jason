import sqlalchemy.orm
from sqlalchemy.ext import declarative

from .config.postgres import PostgresConfigMixin

db = sqlalchemy
orm = sqlalchemy.orm
model_factory = sqlalchemy.ext.declarative.declarative_base
scoped_session = sqlalchemy.orm.scoped_session


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
