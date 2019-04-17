

def maybe_call(value):
    if callable(value):
        return value()
    return value
