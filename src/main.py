from typing import Type

import arcade

from settings.registered_views import RegisteredViews
from src.core.registry import Registry
from src.core.display import BaseWindow, BaseView
from src.services.event_service import EventBus
from src.core.service_container import ServiceContainer

from src.services.input.input_service import InputService
from src.services.navigation_service import NavigationService
from src.settings.game_constants import GameConstants
from src.settings.game_resources import GameResources
from src.services.input.settings.registered_input_contexts import RegisteredInputContexts

from src.views.main_menu_view import MainMenuView
from src.views.game_view import GameView


class MainWindow(BaseWindow):

    def __init__(self, service_container: ServiceContainer):

        super().__init__(
            service_container,
            GameConstants.WINDOW_WIDTH,
            GameConstants.WINDOW_HEIGHT,
            GameConstants.WINDOW_TITLE
        )

        self.service_container = service_container


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
    if not nav_service: raise RuntimeError(f"Required service '{NavigationService.__name__}' is not registered!")

    nav_service.navigate("main_menu")

def run_game():

    GameResources.init()
    RegisteredInputContexts.init()

    view_registry = Registry[Type[BaseView]]()
    service_container = ServiceContainer()

    window = MainWindow(service_container)

    register_views(view_registry)
    init_services(service_container, window, view_registry)

    start_game(service_container)

    arcade.run()


if __name__ == "__main__":
    run_game()