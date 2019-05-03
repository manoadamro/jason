def maybe_call(value):
    if callable(value):
        return value()
    return value


def is_bool(value):
    return type(value) is bool


def is_type(value, typ=None):
    if not isinstance(value, type):
        return False
    if typ is not None and not issubclass(value, typ):
        return False
    return True


def is_instance_or_type(value, typ):
    return is_type(value, typ=typ) or isinstance(value, typ)
