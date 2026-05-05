import inspect
from typing import TypeVar, List, Type

from src.core.display import BaseWindow, BaseView
from src.core.registry import RegistryException
from src.core.service_container import Service

V = TypeVar("V", bound="BaseView")


class NavigationService(Service):

    def __init__(self, window: BaseWindow):
        super().__init__("navigation")

        self._window = window
        self._stack: List[BaseView] = []

        self.current_view = None

    def navigate(self, view_type: Type[V]):
        self._stack.clear()
        self.push(view_type)

    def push(self, view_type: Type[V]):

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

        view_constructor = inspect.signature(view_type.__init__)
        kwargs = {}

        for name, param in view_constructor.parameters.items():

            if name == "self":
                continue

            param_type = param.annotation

            if param_type is inspect.Parameter.empty:

                raise RegistryException(
                    f"Parameter '{name}' in {view_type.__name__} has no type annotation!"
                )

            service = self._window.service_container.get(param_type)
            kwargs[name] = service

        return view_type(**kwargs)