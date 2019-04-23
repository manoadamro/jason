from importlib import import_module as _import

_component_path = "jason.components"


def run(component):
    module = _import(f"{_component_path}.{component}")
    return module.build
