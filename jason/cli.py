from importlib import import_module as _import

_component_path = "jason.components"


def run(component):
    """
    runs a service from the components package by name.
    package must implement `build` method in it's top level

    """
    module = _import(f"{_component_path}.{component}")
    return module.build
