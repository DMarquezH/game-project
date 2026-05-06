import arcade

from src.core.display import BaseWindow
from src.core.event.event_service import EventBus
from src.core.service_container import ServiceContainer
from src.services.input_service import InputService
from src.services.navigation import NavigationService
from src.settings.game_constants import GameConstants
from src.settings.game_resources import GameResources
from src.views.main_menu_view import MainMenuView


class MainWindow(BaseWindow):

    def __init__(self, service_container: ServiceContainer):

        super().__init__(
            service_container,
            GameConstants.WINDOW_WIDTH,
            GameConstants.WINDOW_HEIGHT,
            GameConstants.WINDOW_TITLE
        )

        self.service_container = service_container

    def init_services(self):

        if self.service_container.is_frozen(): return

        self.service_container.register(NavigationService(self))
        self.service_container.register(EventBus())
        self.service_container.register(InputService())

        self.service_container.freeze()


def main():

    GameResources.init()
    service_container = ServiceContainer()

    window = MainWindow(service_container)
    window.init_services()

    nav_service = service_container.get(NavigationService)
    nav_service.navigate(MainMenuView)

    arcade.run()


if __name__ == "__main__":
    main()