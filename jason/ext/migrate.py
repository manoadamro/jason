try:
    import flask_migrate
except (ImportError, ModuleNotFoundError):
    raise ImportError()  # TODO


class Migrate(flask_migrate.Migrate):
    ...
