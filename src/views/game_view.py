import arcade.color
from arcade import Camera2D
from pyglet.math import Vec2

from src.core.display import BaseView, GameCamera
from src.world.world import World


class GameView(BaseView):

    def __init__(self):
        super().__init__()
        self.active_keyboard_inputs = set()
        self.world = World()
        self.hud = None

        self.world_camera = GameCamera(follow_target=self.world.player)
        self.ui_camera = Camera2D()

    def on_show_view(self):
        self.background_color = arcade.color.BLACK

    def on_hide_view(self):
        pass

    def on_draw(self) -> bool | None:
        super().on_draw()

        self.world_camera.use()
        self.world.draw()

        self.ui_camera.use()
        # draw UI

    def on_update(self, delta_time: float) -> bool | None:
        self.check_inputs()
        self.world.update()

        self.world_camera.update(delta_time)

    def check_inputs(self):
        self.check_player_movement()

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

        self.world.move_player(Vec2(x, y).normalize())

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        self.active_keyboard_inputs.add(symbol)

    def on_key_release(self, symbol: int, modifiers: int) -> bool | None:
        self.active_keyboard_inputs.discard(symbol)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        pass

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        pass