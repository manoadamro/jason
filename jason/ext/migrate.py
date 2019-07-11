try:
    import flask_migrate
except (ImportError, ModuleNotFoundError):
    raise ImportError(
        "package 'flask_migrate' is not installed.\nYou can install it with:\npip3 install flask_migrate"
    )


class Migrate(flask_migrate.Migrate):
    ...
