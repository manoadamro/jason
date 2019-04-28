import os
from importlib import import_module as _import

import fire


class CommandLineInterface:
    @classmethod
    def run(cls, component):
        """
        runs a service from the components package by name.
        package must implement `build` method in it's top level

        """
        component = component.replace("/", ".")

        try:
            module = _import(component)
        except (ModuleNotFoundError, ImportError) as ex:
            raise ImportError(f"could not import {component} from {os.getcwd()}. {ex}")

        main = getattr(module, "main")
        if not main:
            raise AttributeError(
                f"module {component} does not contain a 'main' method {dir(module)}"
            )

        return main


if __name__ == "__main__":
    fire.Fire(CommandLineInterface, name="jason")
