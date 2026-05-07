import arcade.color
from arcade import Camera2D
from pyglet.math import Vec2

from src.core.display import BaseView, GameCamera
from src.services.event_service import EventBus

from src.services.input_service import InputService
from src.services.navigation import NavigationService

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
        self.pause_menu = PauseController(self)

        self.world_camera = GameCamera(follow_target=self.world.player)
        self.ui_camera = Camera2D()


    def on_show_view(self):
        self.background_color = arcade.color.BLACK
        self.hud.enable()
    def on_hide_view(self):
        self.hud.disable()

    def on_draw(self) -> bool | None:
        super().on_draw()

        self.world_camera.use()
        self.world.draw()

        self.ui_camera.use()
        self.hud.draw()

        if self.pause_menu.get_status():
            self.pause_menu.draw()

    def on_update(self, delta_time: float) -> bool | None:
        self.check_inputs()
        self.world.update()

        self.world_camera.update(delta_time)

    def check_inputs(self):
        if not self.pause_menu.get_status():
            self.check_player_movement()
        self.check_pause()

    def check_player_movement(self):

        x, y = 0, 0

        if arcade.key.W in self.active_keyboard_inputs:
            y += 1
        if arcade.key.S in self.active_keyboard_inputs:
            y -= 1

        if arcade.key.D in self.active_keyboard_inputs:
            x += 1
        if arcade.key.A in self.active_keyboard_inputs:
            x -= 1

        self.world.player.move(Vec2(x, y).normalize())

    def check_pause(self):
        if arcade.key.ESCAPE in self.active_keyboard_inputs:
            self.pause_menu.enable()
            self.world.freeze()

    def on_key_press(self, symbol: int, modifiers: int):
        super().on_key_press(symbol, modifiers)
        self.active_keyboard_inputs.add(symbol)

    def on_key_release(self, symbol: int, modifiers: int):
        super().on_key_release(symbol, modifiers)
        self.active_keyboard_inputs.discard(symbol)