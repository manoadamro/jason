import os
from importlib import import_module as _import

import fire

from jason.service import Service


class CLI:
    @classmethod
    def run_service(cls, component):
        """
        runs a service from the components package by name.
        package must implement `build` method in it's top level

        """
        component = component.replace("/", ".")

        try:
            module = _import(component)
        except (ModuleNotFoundError, ImportError) as ex:
            raise ImportError(f"could not import {component} from {os.getcwd()}. {ex}")

        service = None
        for item in dir(module):
            attr = getattr(module, item)
            if isinstance(attr, Service):
                # TODO found service {item}
                service = attr
                break
        if not service:
            raise AttributeError(
                f"module {component} does not contain an instance '{Service.__name__}'"
            )

        return service


if __name__ == "__main__":
    fire.Fire(CLI.run_service, name="jason")
