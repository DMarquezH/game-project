import arcade
from arcade import Camera2D

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


class GameCamera:

    def __init__(self, follow_target: arcade.Sprite | None = None, follow_lerp: float = 0.1):
        self._cam = Camera2D()

        self.follow_target = follow_target
        self.follow_lerp = follow_lerp

        self._counter = 0
        self._shake_intensity = 0

    def update(self, delta_time: float):
        if self.follow_target:
            self.update_pos(delta_time)

    def update_pos(self, delta_time: float):

        target_pos = self.follow_target.position
        current_pos = self._cam.position

        lerp_factor = 1 - pow(1 - self.follow_lerp, delta_time * 60)

        self._cam.position = current_pos.lerp(target_pos, lerp_factor)

    def use(self):
        self._cam.use()