from typing import Type

import arcade

from services.input.settings.registered_input_events import ToggleFullscreenInputEvent
from settings.registered_views import RegisteredViews
from core.registry import Registry
from core.display import BaseWindow, BaseView
from services.event_service import EventBus
from core.service_container import ServiceContainer

from services.input.input_service import InputService
from services.navigation_service import NavigationService
from settings.game_constants import GameConstants
from settings.game_resources import GameResources
from services.input.settings.registered_input_contexts import RegisteredInputContexts

from views.main_menu_view import MainMenuView
from views.game_view import GameView


class MainWindow(BaseWindow):

    def __init__(self, service_container: ServiceContainer):

        super().__init__(
            service_container,
            GameConstants.WINDOW_WIDTH,
            GameConstants.WINDOW_HEIGHT,
            GameConstants.WINDOW_TITLE
        )

        self.center_window()

    def init(self):
        event_bus = self.service_container.get(EventBus)
        event_bus.subscribe(ToggleFullscreenInputEvent, self._toggle_fullscreen)

    def _toggle_fullscreen(self, _: ToggleFullscreenInputEvent):
        self.set_fullscreen(not self.fullscreen)


def register_views(view_registry: Registry[Type[BaseView]]):

    if view_registry.is_frozen(): return

    view_registry.register(RegisteredViews.MAIN_MENU, MainMenuView)
    view_registry.register(RegisteredViews.GAME, GameView)

    view_registry.freeze()

def init_services(service_container: ServiceContainer, window: MainWindow, view_registry: Registry[Type[BaseView]]):

    if service_container.is_frozen(): return

    nav_service = NavigationService(window, service_container, view_registry)
    event_bus = EventBus()
    input_service = InputService(event_bus)

    service_container.register(nav_service)
    service_container.register(event_bus)
    service_container.register(input_service)

    service_container.freeze()

def start_game(service_container: ServiceContainer):

    nav_service = service_container.get(NavigationService)
    input_service = service_container.get(InputService)

    if not nav_service:
        raise RuntimeError(f"Required service '{NavigationService.__name__}' is not registered!")

    if not input_service:
        raise RuntimeError(f"Required service '{InputService.__name__}' is not registered!")

    input_service.enable_context(RegisteredInputContexts.GENERAL)
    nav_service.navigate("main_menu")

def run_game():

    GameResources.init()
    RegisteredInputContexts.init()

    view_registry = Registry[Type[BaseView]]()
    service_container = ServiceContainer()

    window = MainWindow(service_container)

    register_views(view_registry)
    init_services(service_container, window, view_registry)

    window.init()

    start_game(service_container)

    arcade.run()


if __name__ == "__main__":
    run_game()