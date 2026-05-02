import arcade.color
from pyglet.math import Vec2

from src.core.display import BaseView
from src.world.world import World


class GameView(BaseView):

    def __init__(self):
        super().__init__()
        self.inputs = set()
        self.world = World()
        self.hud = None

    def on_show_view(self):
        self.background_color = arcade.color.BLACK

    def on_hide_view(self):
        pass

    def on_draw(self) -> bool | None:
        super().on_draw()
        self.world.draw()

    def on_update(self, delta_time: float) -> bool | None:
        self.check_inputs()
        self.world.update()

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        self.inputs.add(symbol)

    def on_key_release(self, symbol: int, modifiers: int) -> bool | None:
        self.inputs.discard(symbol)

    def check_inputs(self):

        x, y = 0, 0

        if arcade.key.W in self.inputs:
            y += 1
        if arcade.key.S in self.inputs:
            y -= 1

        if arcade.key.D in self.inputs:
            x += 1
        if arcade.key.A in self.inputs:
            x -= 1

        self.world.move_player(Vec2(x, y).normalize())