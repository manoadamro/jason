from .property import Property


class Model:
    __strict__ = True
    __props__ = None

    def __init_subclass__(cls):
        props = {}
        for field in dir(cls):
            if field.startswith("_"):
                continue
            value = getattr(cls, field)
            if isinstance(value, type) and issubclass(value, Property):
                props[field] = value()
            if isinstance(value, Property):
                props[field] = value
        cls.__props__ = props
