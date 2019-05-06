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


def deep_compare(base, compare):
    if not hasattr(base, "__dict__") or not hasattr(compare, "__dict__"):
        return base == compare
    if len(base.__dict__) != len(compare.__dict__):
        return False
    for key, value in base.__dict__.items():
        if key not in compare.__dict__:
            return False
        if not deep_compare(value, compare.__dict__[key]):
            return False
    return True
