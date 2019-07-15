import importlib
import os

from jason.service import Service


class CLI:

    @classmethod
    def service(cls, service):
        service = service.replace("/", ".")

        if ":" in service:
            service, service_name = service.split(":")
        else:
            service_name = None

        try:
            module = importlib.import_module(service)
        except (ModuleNotFoundError, ImportError) as ex:
            raise ImportError(f"could not import {service} from {os.getcwd()}. {ex}")

        if service_name:
            service = getattr(module, service_name, None)
            if not service:
                raise AttributeError(
                    f"module {service} does not contain a service called or assigned to 'service_name'"
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
                    f"module {service} does not contain an instance '{Service.__name__}'"
                )

        return service
