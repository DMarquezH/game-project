import arcade

from src.core.service_container import ServiceContainer


class BaseWindow(arcade.Window):

    def __init__(self, service_container: ServiceContainer, width: float, height: float, title: str):
        super().__init__(width, height, title)
        self.service_container = service_container

    def init_services(self):
        self.service_container.freeze()


class BaseView(arcade.View):

    def __init__(self):
        super().__init__()

    def on_draw(self) -> bool | None:
        self.clear()