import arcade
import arcade.gui as gui
from core.display import BaseView
from services.event_service import EventBus
from services.input.input_service import InputService
from services.navigation_service import NavigationService
from settings.game_resources import GameResources
from ui.widgets.base_button import BaseButton


class GameOverView(BaseView):
    def __init__(self,input_service: InputService, nav_service: NavigationService, event_bus: EventBus):
        super().__init__(input_service)
        self.manager = gui.UIManager()

        self.image_background = arcade.load_texture(GameResources.get("textures") /"ui"/"menus"/"gameover_background.png")
        self.button = BaseButton(GameResources.get("textures") /"ui"/"menus"/"button_menu_principal_spritesheet.png",event_bus,x=0,y=100,image_width=300,image_height=138,columns=2,count=2,action= lambda: nav_service.navigate("main_menu"))
        self.manager.add(self.button)
    def on_show_view(self):
        super().on_show_view()
        self.manager.enable()
        self.button.center_x = self.window.get_size()[0] / 2
    def on_hide_view(self):
        super().on_hide_view()
        self.manager.disable()
    def _draw_image(self):
        arcade.draw_texture_rect(
            texture=self.image_background,
            rect=arcade.XYWH(self.window.get_size()[0] / 2, self.window.get_size()[1] / 2, self.window.get_size()[0],
                             self.window.get_size()[1]),
        )

    def on_draw(self):
        super().on_draw()
        self.clear()

        self._draw_image()
        self.manager.draw()