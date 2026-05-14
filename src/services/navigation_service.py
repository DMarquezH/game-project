import inspect
from inspect import Signature
from typing import TypeVar, List, Type, Dict

from core.display import BaseWindow, BaseView
from core.registry import RegistryException, Registry
from core.service_container import Service, ServiceContainer

V = TypeVar("V", bound="BaseView")


class NavigationService(Service):

    def __init__(self, window: BaseWindow, service_container: ServiceContainer, view_registry: Registry[Type[V]]):
        super().__init__("navigation")

        self._service_container = service_container
        self._view_registry = view_registry

        self._constructor_cache: Dict[Type[V], Signature] = {}

        self._window = window
        self._stack: List[BaseView] = []

        self.current_view = None

    def navigate(self, view_key: str):
        self._stack.clear()
        self.push(view_key)

    def push(self, view_key: str):

        view_type = self._view_registry.get(view_key)

        if not view_type:
            raise RegistryException(f"View {view_key} is not registered!")

        view = self._resolve_services(view_type)

        self._stack.append(view)
        self.current_view = view

        self._window.show_view(view)

    def pop(self):

        if len(self._stack) < 2: return

        self._stack.pop()
        view = self._stack[-1]

        self.current_view = view
        self._window.show_view(self._stack[-1])

    def _resolve_services(self, view_type: Type[V]) -> V:

        view_constructor = self._constructor_cache.get(
            view_type,
            inspect.signature(view_type.__init__)
        )
        self._constructor_cache[view_type] = view_constructor

        kwargs = {}

        for name, param in view_constructor.parameters.items():

            if name == "self":
                continue

            param_type = param.annotation

            if param_type is inspect.Parameter.empty:

                raise RegistryException(
                    f"Parameter '{name}' in {view_type.__name__} has no type annotation!"
                )

            service = self._service_container.get(param_type)

            if not service:
                raise RegistryException(f"Service of type '{param_type.__name__}' is not registered!")

            kwargs[name] = service

        return view_type(**kwargs)