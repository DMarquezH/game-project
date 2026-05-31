import arcade
import arcade.gui as gui
from arcade.gui import UIManager

from core.display import BaseView
from services.input.input_service import InputService
from services.navigation_service import NavigationService
from services.event_service import EventBus
from settings.registered_gameplay_events import GameStartedEvent, PlayMusicEvent
from settings.game_resources import GameResources
from settings.registered_views import RegisteredViews
from ui.grid_button_builder import GridButtons


class MainMenuView(BaseView):
    """
    Main menus containing background and main buttons
    """

    def __init__(self, input_service: InputService, nav_service: NavigationService, event_bus: EventBus):
        super().__init__(input_service)

        self.event_bus = event_bus
        self.nav_service = nav_service
        self.ui = UIManager()

        menu_textures = GameResources.get("textures") / "ui" / "menus"
        sounds = GameResources.get("sounds")

        self.button_data = [
            {
                "sheet": menu_textures / "button_jugar_spritesheet.png",
                "action": self._start_game,
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
        self.box = gui.UIBoxLayout(vertical=True, space_between=200).with_padding(top=100)
        image_logo = arcade.load_texture(menu_textures / "logo.png")
        self.logo = gui.UIImage(texture=image_logo,width=image_logo.width/2,height=image_logo.height/2)
        self.botones = GridButtons(self.button_data, space_between=50, event_bus=self.event_bus)
        self.imagen: arcade.Texture = arcade.load_texture(menu_textures / "main_menu_background.png")
        self.event_bus.dispatch(PlayMusicEvent("soundtrack1"))

        self.box.add(self.logo)
        self.box.add(self.botones)

        self.anchor = gui.UIAnchorLayout()
        self.anchor.add(self.box,anchor_x="center",anchor_y="top")

        self.ui.add(self.anchor)

    def _start_game(self):
        self.event_bus.dispatch(GameStartedEvent())
        self.nav_service.navigate(RegisteredViews.GAME)

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