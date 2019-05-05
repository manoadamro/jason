from jason import mixins
try:
    import flask_sqlalchemy
except ImportError:
    raise ImportError()  # TODO


class SQLAlchemy(flask_sqlalchemy.SQLAlchemy):

    def init_app(self, app, migrate=None):
        app.assert_mixin(mixins.PostgresConfigMixin, "database")
        app.config["SQLALCHEMY_DATABASE_URI"] = self._database_uri(app.config, app.testing)
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
        if config.DB_USER:
            credentials = f"{config.DB_USER}:{config.DB_PASS}@"
        else:
            credentials = ""
        return (
            f"{config.DB_DRIVER}://{credentials}"
            f"{config.DB_HOST}:{config.DB_PORT}"
            f"/{config.DB_NAME}"
        )
