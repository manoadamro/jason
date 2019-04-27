import functools
import logging
import os
from importlib import import_module as _import
from typing import Type

import fire

from jason.service import Service
from jason.utils import is_type

logger = logging.getLogger("jason-cli")


class CommandLineInterface:
    @staticmethod
    def _find_service(module, default=None) -> Type[Service]:
        obj = default
        for name in dir(module):
            if name.startswith("_"):
                continue
            obj = getattr(module, name, None)
            if not is_type(obj, typ=Service):
                continue
            break
        return obj

    @classmethod
    def run(cls, component):
        """
        runs a service from the components package by name.
        package must implement `build` method in it's top level

        """
        component = component.replace("/", ".")

        logger.info("running component %s", component)

        module = _import(component)
        if not module:
            raise ImportError(f"could not import {component} from {os.getcwd()}")

        service_class = cls._find_service(module, default=None)
        if not service_class:
            raise AttributeError(
                f"module {component} does not contain a subclass of {Service.__name__} {dir(module)}"
            )

        @functools.wraps(service_class)
        def wrapped(*args, **kwargs):
            """
            required to make fire use the params from the service constructor and call start

            """
            logger.info("starting component %s", component)
            service = service_class(*args, **kwargs)
            service.start()

        return wrapped


if __name__ == "__main__":
    fire.Fire(CommandLineInterface, name="jason")
