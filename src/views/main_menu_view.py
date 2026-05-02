from pathlib import Path

import arcade
from arcade.gui import UIManager

from src.core.display import BaseView
from src.services.navigation import NavigationService
from src.ui.grid_button_builder import GridButtons
from src.views.game_view import GameView


class MainMenuView(BaseView):
    """
    Main menus containing background and main buttons
    """

    def __init__(self, nav_service: NavigationService):
        super().__init__()

        self.ui = UIManager()

        menu_textures: Path = arcade.resources.resolve(":textures:") / "ui" / "menus"

        self.button_data = [
            {
                "sheet": menu_textures / "button_jugar_spritesheet.png",
                "action": lambda: nav_service.navigate(GameView),
                "width": 300,
                "height": 138,
                "columns": 2,
                "count": 2,
            },
            {
                "sheet": menu_textures / "button_opciones_spritesheet.png",
                "action": None,
                "width": 300,
                "height": 138,
                "columns": 2,
                "count": 2,
            },
            {
                "sheet": menu_textures / "button_salir_spritesheet.png",
                "action": lambda: arcade.close_window(),
                "width": 300,
                "height": 138,
                "columns": 2,
                "count": 2,
            }
        ]

        self.botones = GridButtons(self.button_data, space_between=50)
        self.imagen: arcade.Texture = arcade.load_texture(menu_textures / "main_menu_background.png")

        self.ui.add(self.botones)

    def draw_imagen(self):
        arcade.draw_texture_rect(
            texture=self.imagen,
            rect=arcade.XYWH(self.window.get_size()[0] / 2, self.window.get_size()[1] / 2, self.window.get_size()[0],
                             self.window.get_size()[1]),
        )

    def on_show_view(self):
        super().on_show_view()
        self.ui.enable()
        arcade.set_background_color(arcade.color.WHITE)

    def on_hide_view(self) -> None:
        self.ui.disable()

    def on_draw(self):
        self.clear()
        self.draw_imagen()
        self.ui.draw()