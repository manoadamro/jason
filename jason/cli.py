import importlib
import os

from jason.service import Service


class CLI:
    @classmethod
    def service(cls, component):
        component = component.replace("/", ".")

        if ":" in component:
            component, service_name = component.split(":")
        else:
            service_name = None

        try:
            module = importlib.import_module(component)
        except (ModuleNotFoundError, ImportError) as ex:
            raise ImportError(f"could not import {component} from {os.getcwd()}. {ex}")

        if service_name:
            service = getattr(module, service_name, None)
            if not service:
                raise AttributeError(
                    f"module {component} does not contain a service called or assigned to 'service_name'"
                )
        else:
            service = None
            for item in dir(module):
                attr = getattr(module, item)
                if isinstance(attr, Service):
                    service = attr
                    break
            if not service:
                raise AttributeError(
                    f"module {component} does not contain an instance '{Service.__name__}'"
                )

        return service
