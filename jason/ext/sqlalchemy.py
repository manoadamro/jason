import functools

from jason import mixins

try:
    import flask_sqlalchemy
except ImportError:
    raise ImportError()  # TODO


class SQLAlchemy(flask_sqlalchemy.SQLAlchemy):
    def init_app(self, app, migrate=None):
        app.assert_mixin(mixins.PostgresConfigMixin, "database")
        app.config["SQLALCHEMY_DATABASE_URI"] = self._database_uri(
            app.config, app.testing
        )
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        super(SQLAlchemy, self).init_app(app)
        if migrate is not None:
            migrate.init_app(app=app, db=self)
        if app.testing:
            with app.app_context():
                self.create_all()

    @staticmethod
    def _database_uri(config, testing=False):
        if testing:
            return config.TEST_DB_URL
        credentials = []
        if config.DB_USER or config.DB_PASS:
            if config.DB_USER:
                credentials.append(config.DB_USER)
            credentials.append(":")
            if config.DB_PASS:
                credentials.append(config.DB_PASS)
            credentials.append("@")
        credentials = ''.join(credentials)
        if config.DB_NAME:
            db_name = f"/{config.DB_NAME}"
        else:
            db_name = ""
        db_host = config.DB_HOST
        if config.DB_PORT:
            db_host += f":{config.DB_PORT}"
        string = (
            f"{config.DB_DRIVER}://{credentials}"
            f"{db_host}"
            f"{db_name}"
        )
        print(string)
        return string

    @staticmethod
    def serializable(*names):
        def wrap(func):
            class Wrapped(func):
                def to_dict(self):
                    return {name: getattr(self, name) for name in names}

            return Wrapped

        return wrap
