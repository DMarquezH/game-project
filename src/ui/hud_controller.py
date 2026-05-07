import arcade
import arcade.gui
from ui.game_hud import GameHud
from ui.base_gui_controller import BaseGuiController


class HudController(BaseGuiController):
    def __init__(self):
        super().__init__()

        coin_rute = arcade.resources.resolve(":textures:") / "ui" / "hud" / "coin_highres.png"
        heart_rute = arcade.resources.resolve(":textures:") / "ui" / "hud" / "heart_highres.png"

        config_hud = [ {"id":"health","image":heart_rute,"text":f"100/100"}, {"id":"coins","image":coin_rute,"text":"0"}]

        self.hud = GameHud(config_hud)
        self.manager.add(self.hud)

    def set_coins(self,coins:int):
        self.hud.set_text("coins", f"{coins}")

    def set_health(self,health:int):
        self.hud.set_text("health", f"{health}/100")


