from calendar import TUESDAY

import arcade
from arcade import Camera2D

from core.service_container import ServiceContainer
from services.input.devices.keyboard_device import KeyboardInputDevice
from services.input.devices.mouse_device import MouseInputDevice
from services.input.input_service import InputService



class BaseWindow(arcade.Window):

    def __init__(self, service_container: ServiceContainer, width: int, height: int, title: str):
        super().__init__(width, height, title)
        self.service_container = service_container
        self.set_fullscreen(True)


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

    def __init__(
            self,
            follow_target: arcade.Sprite = None,
            follow_lerp: float = 0.1,
            clamp_rect: arcade.Rect = None
    ):
        self.cam = Camera2D()

        self.follow_target = follow_target
        self.follow_lerp = follow_lerp

        self.clamp_rect = clamp_rect

    def update(self, delta_time: float):

        if self.follow_target is not None:
            self._update_pos(delta_time)

        if self.clamp_rect is not None:
            self._clamp_pos()

    def _update_pos(self, delta_time: float):

        target_pos = self.follow_target.position
        current_pos = self.cam.position

        lerp_factor = 1 - pow(1 - self.follow_lerp, delta_time * 60)

        self.cam.position = current_pos.lerp(target_pos, lerp_factor)

    def use(self):
        self.cam.use()

    def _clamp_pos(self):

        x, y = self.cam.position
        viewport = self.cam.viewport

        half_w = viewport.width / 2
        half_h = viewport.height / 2

        min_x = self.clamp_rect.left + half_w
        max_x = self.clamp_rect.right - half_w

        min_y = self.clamp_rect.bottom + half_h
        max_y = self.clamp_rect.top - half_h

        clamped_x = max(min_x, min(x, max_x))
        clamped_y = max(min_y, min(y, max_y))

        self.cam.position = arcade.Vec2(clamped_x, clamped_y)