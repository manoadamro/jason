try:
    import kombu
except (ImportError, ModuleNotFoundError):
    raise ImportError(
        "package 'kombu' is not installed.\nYou can install it with:\npip3 install kombu"
    )
