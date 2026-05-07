from src.settings.game_resources import GameResources
from src.ui.grid_button_builder import GridButtons
from src.ui.base_gui_controller import BaseGuiController
from src.settings.game_views import Views


class PauseController(BaseGuiController):
    def __init__(self,view):
        super().__init__()
        self.enabled = False
        self.current_view = view

        menu_textures = GameResources.get("textures") / "ui" / "menus"
        sounds = GameResources.get("sounds")

        button_list = [
            {
                "sheet": menu_textures / "button_reanudar_spritesheet.png",
                "sound": sounds / "menu_button.wav",
                "action": lambda : unpause(self.current_view),
                "width": 300,
                "height": 138,
                "columns": 2,
                "count": 2,
            },
            {
                "sheet": menu_textures / "button_opciones_spritesheet.png",
                "sound": sounds / "menu_button.wav",
                "action": None,
                "width": 300,
                "height": 138,
                "columns": 2,
                "count": 2,
            },
            {
                "sheet": menu_textures / "button_menu_principal_spritesheet.png",
                "sound": sounds / "menu_button.wav",
                "action": lambda: self.current_view.nav_service.navigate(Views.MAIN_MENU),
                "width": 300,
                "height": 138,
                "columns": 2,
                "count": 2,
            }

        ]
        self.botones = GridButtons(button_list,space_between=50,background=menu_textures / "pause_background.png")
        self.manager.add(self.botones)

    def enable(self):
        super().enable()
        self.enabled = True

    def disable(self):
        super().disable()
        self.enabled = False

    def is_enabled(self):
        return self.enabled

def unpause(view):
    view.pause_menu.disable()