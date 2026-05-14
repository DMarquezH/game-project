from typing import TypeVar, Dict, Type

from core.registry import RegistryException, Freezable

S = TypeVar("S", bound="Service")


class Service:

    def __init__(self, name: str):
        self.name = name


class ServiceContainer(Freezable):

    def __init__(self):
        super().__init__()
        self._services: Dict[Type[Service], Service] = {}

    def register(self, service: S):

        if self._frozen:
            raise RegistryException("Service container is frozen!")

        service_type = type(service)

        if service_type in self._services:
            raise RegistryException(f"Service of type '{service_type.__name__}' is already registered!")

        self._services[service_type] = service

    def get(self, service_type: Type[S]) -> S | None:

        service = self._services.get(service_type)

        if service is None:
            raise RegistryException(f"No registered services found for type: {service_type.__name__}")

        return service