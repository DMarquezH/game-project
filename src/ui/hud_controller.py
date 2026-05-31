import arcade
import arcade.gui

from entities.player_entity import Player
from services.event_service import BaseEvent
from settings.game_resources import GameResources
from ui.widgets.game_hud import GameHud
from ui.base_gui_controller import BaseGuiController
from ui.widgets.stat_widget import StatWidget
from ui.widgets.wave_widget import WaveWidget
from world.systems.combat.entity_stats import EntityStats
from world.systems.enemy_wave_system import WaveCompleteEvent


class HudController(BaseGuiController):
    def __init__(self,stats:EntityStats):
        super().__init__()

        coin_rute = GameResources.get("textures") / "ui" / "hud" / "coin_highres.png"
        heart_rute = GameResources.get("textures") / "ui" / "hud" / "heart_highres.png"

        config_hud = [ {"id":"health","image":heart_rute,"text":f"100/100"}, {"id":"coins","image":coin_rute,"text":"0"}]

        self.hud = GameHud(config_hud)
        self.wave = WaveWidget()
        self.stats = StatWidget(stats)
        self.manager.add(self.hud)
        self.manager.add(self.wave)
        self.manager.add(self.stats)

    def set_coins(self,coins:int):
        self.hud.set_text("coins", f"{coins}")

    def set_health(self, health: int, max_health: int = 100):
        self.hud.set_text("health", f"{health}/{max_health}")

    def update_wave(self, event: WaveCompleteEvent):
        self.wave.update_wave()

    def update_stats(self, player: Player):
        self.stats.update_stats(player.stats)

