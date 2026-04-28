from pathlib import Path

import arcade
import arcade.gui

from src.base.event import EventBus
from src.service.input import InputService
from src.ui.grid_button_builder import GridButtons

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

WINDOW_TITLE = "survivor-project v0.1"

PROJECT_PATH = Path(__file__).parent.parent.parent.resolve()
TEXTURE_PATH = PROJECT_PATH / "assets" / "textures"

class GameView(arcade.View):

    def __init__(self, event_bus: EventBus, input_service: InputService):
        super().__init__()
        self._event_bus = event_bus
        self._input = input_service

    def on_show_view(self):
        print("GameView")

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        self._input.register_input(symbol)

    def on_key_release(self, symbol: int, modifiers: int) -> bool | None:
        self._input.remove_input(symbol)

    def on_update(self, delta_time: float) -> bool | None:
        pass

    def on_draw(self) -> bool | None:
        pass

class MenuView(arcade.gui.UIView):
    """
    Main menu containing background and main buttons
    """
    def __init__(self):
        super().__init__()
        self.button_data = [
            {
                "sheet": TEXTURE_PATH / "menu" / "button_jugar_spritesheet.png",
                "action": lambda: arcade.get_window().show_view(GameView(EventBus(),InputService())),
                "width": 300,
                "height": 138,
                "columns": 2,
                "count": 2,
            },
            {
                "sheet": TEXTURE_PATH / "menu" / "button_opciones_spritesheet.png",
                "action": None,
                "width": 300,
                "height": 138,
                "columns": 2,
                "count": 2,
            },
            {
                "sheet": TEXTURE_PATH / "menu" / "button_salir_spritesheet.png",
                "action": lambda: arcade.close_window(),
                "width": 300,
                "height": 138,
                "columns": 2,
                "count": 2,
            }
        ]
        self.botones = GridButtons(self.button_data,space_between=50)
        self.ui.add(self.botones)

        self.imagen : arcade.Texture = arcade.load_texture(TEXTURE_PATH / "menu" / "main_menu_background.png")

    def draw_imagen(self):

        arcade.draw_texture_rect(
            texture=self.imagen,
            rect=arcade.XYWH(self.window.get_size()[0]/2,self.window.get_size()[1]/2,self.window.get_size()[0],self.window.get_size()[1]),

        )

    def on_show_view(self):
        super().on_show_view()
        arcade.set_background_color(arcade.color.WHITE)



    def on_draw(self):
        self.clear()
        self.draw_imagen()
        self.ui.draw()

def main():

    input_service = InputService()

    window = arcade.Window()
    view = MenuView()
    #view = GameView(EventBus(), input_service)

    window.show_view(view)
    arcade.run()


if __name__ == '__main__':
    main()