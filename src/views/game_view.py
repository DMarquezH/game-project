import arcade.color
from arcade import Camera2D

from src.core.display import BaseView, GameCamera
from src.services.event_service import EventBus
from src.services.input.devices.mouse_device import MouseInputDevice

from src.services.input.input_service import InputService
from src.services.navigation_service import NavigationService
from src.services.input.settings.registered_input_contexts import RegisteredInputContexts
from src.services.input.settings.registered_input_events import TogglePauseInputEvent

from src.world.world import World
from src.ui.hud_controller import HudController
from src.ui.pause_controller import PauseController


class GameView(BaseView):

    def __init__(self, input_service: InputService, event_bus: EventBus, nav_service: NavigationService):
        super().__init__(input_service)

        self.event_bus = event_bus
        self.nav_service = nav_service

        self.active_keyboard_inputs = set()
        self.world = World(event_bus)
        self.hud = HudController()
        self.pause_menu = PauseController(self, event_bus)

        self.world_camera = GameCamera(follow_target=self.world.player)
        self.ui_camera = Camera2D()

        self._subscribe_listeners()

    def _subscribe_listeners(self):
        self.event_bus.subscribe(TogglePauseInputEvent, self.on_toggle_pause)

    def _unsubscribe_listeners(self):
        self.event_bus.unsubscribe(TogglePauseInputEvent, self.on_toggle_pause)

    def on_show_view(self):

        self.input_service.enable_context(RegisteredInputContexts.GAMEPLAY)
        self.input_service.enable_context(RegisteredInputContexts.DEBUG)

        self.background_color = arcade.color.BLACK
        self.hud.enable()

    def on_hide_view(self):

        self._unsubscribe_listeners()

        self.input_service.disable_context(RegisteredInputContexts.GAMEPLAY)
        self.input_service.disable_context(RegisteredInputContexts.DEBUG)

        self.hud.disable()
        self.pause_menu.disable()

        self.world.dispose()

    def on_update(self, dt: float):
        super().on_update(dt)

        if not self.pause_menu.is_enabled():
            self.world.update()
            self.world_camera.update(dt)

    def on_draw(self):
        super().on_draw()

        self.world_camera.use()
        self.world.draw()

        self.ui_camera.use()
        self.hud.draw()

        if self.pause_menu.is_enabled():
            self.pause_menu.draw()

    def on_toggle_pause(self, _: TogglePauseInputEvent):

        if self.pause_menu.is_enabled():
            self.unpause()
        else:
            self.pause()

    def pause(self):

        self.input_service.enable_context(RegisteredInputContexts.PAUSE)

        self.input_service.disable_context(RegisteredInputContexts.GAMEPLAY)
        self.input_service.disable_context(RegisteredInputContexts.DEBUG)

        self.pause_menu.enable()

    def unpause(self):

        self.input_service.enable_context(RegisteredInputContexts.GAMEPLAY)
        self.input_service.enable_context(RegisteredInputContexts.DEBUG)

        self.input_service.disable_context(RegisteredInputContexts.PAUSE)

        self.pause_menu.disable()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):

        in_world_coords = self.world_camera.cam.unproject((x, y)).xy

        inp = MouseInputDevice.from_button(
            button,
            in_world_coords.x, in_world_coords.y
        )

        self.input_service.register_press(inp)