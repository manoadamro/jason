import sqlalchemy.orm
from sqlalchemy.ext import declarative

from jason.config import Config, props

Config = Config
props = props

db = sqlalchemy
orm = sqlalchemy.orm
model_factory = sqlalchemy.ext.declarative.declarative_base


class PostgresConfigMixin:
    DB_DRIVER = props.String(default="postgresql")
    DB_HOST = props.String()
    DB_PORT = props.String()
    DB_USER = props.String(nullable=True)
    DB_PASS = props.String(nullable=True)
    TEST_DB_URL = props.String(default="sqlite:///:memory:")


class Database:
    session_maker = sqlalchemy.orm.sessionmaker()

    def __init__(self):
        self._session = self.session_maker()

    def session(self):
        return sqlalchemy.orm.scoped_session(self._session)

    @classmethod
    def _engine(cls, config: PostgresConfigMixin, testing=False):
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

    def init(self, config, testing=False):
        engine = self._engine(config=config, testing=testing)
        self._session.configure(bind=engine)
