import arcade
from arcade import Camera2D

from src.core.service_container import ServiceContainer
from src.services.input.devices.keyboard_device import KeyboardInputDevice
from src.services.input.devices.mouse_device import MouseInputDevice
from src.services.input.input_service import InputService


class BaseWindow(arcade.Window):

    def __init__(self, service_container: ServiceContainer, width: int, height: int, title: str):
        super().__init__(width, height, title)
        self.service_container = service_container

    def init_services(self):
        self.service_container.freeze()


class BaseView(arcade.View):

    def __init__(self, input_service: InputService):
        super().__init__()
        self.input_service = input_service

    def on_update(self, dt: float):
        self.input_service.update()

    def on_draw(self):
        self.clear()

    def on_key_press(self, symbol: int, modifiers: int):
        inp = KeyboardInputDevice.from_key(symbol)
        self.input_service.register_press(inp)

    def on_key_release(self, symbol: int, modifiers: int):
        inp = KeyboardInputDevice.from_key(symbol)
        self.input_service.register_release(inp)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        inp = MouseInputDevice.from_button(button, x, y)
        self.input_service.register_press(inp)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        inp = MouseInputDevice.from_button(button, x, y)
        self.input_service.register_release(inp)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        inp = MouseInputDevice.from_scroll(x, y, scroll_x, scroll_y)
        self.input_service.register_change(inp)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        inp = MouseInputDevice.from_motion(x, y, dx, dy)
        self.input_service.register_change(inp)

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, button: int, _modifiers: int):
        inp = MouseInputDevice.from_drag(button, x, y, dx, dy)
        self.input_service.register_change(inp)


class GameCamera:

    def __init__(self, follow_target: arcade.Sprite | None = None, follow_lerp: float = 0.1):
        self.cam = Camera2D()

        self.follow_target = follow_target
        self.follow_lerp = follow_lerp

    def update(self, delta_time: float):
        if self.follow_target:
            self.update_pos(delta_time)

    def update_pos(self, delta_time: float):

        target_pos = self.follow_target.position
        current_pos = self.cam.position

        lerp_factor = 1 - pow(1 - self.follow_lerp, delta_time * 60)

        self.cam.position = current_pos.lerp(target_pos, lerp_factor)

    def use(self):
        self.cam.use()