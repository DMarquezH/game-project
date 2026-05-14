import arcade
from world.level.base_level import BaseLevel
from settings.game_resources import GameResources

class LevelLoader:

    def __init__(self, level: BaseLevel):
        self.tile_map    = arcade.load_tilemap(level.tilemap_path, scaling=1, layer_options=level.layer_options)
        self.texture     = arcade.load_texture(GameResources.get("textures") / "entity" / "player_highres.png")
        self.player_start    = BaseLevel.player_start(self, self.tile_map)
        self.collision_layers = level.collision_layers