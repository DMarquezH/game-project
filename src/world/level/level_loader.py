import arcade
from world.level.base_level import BaseLevel
from settings.game_resources import GameResources

class LevelLoader:

    def __init__(self, level: BaseLevel):
        self.tile_map    = arcade.load_tilemap(level.tilemap_path, scaling=1, layer_options=level.layer_options)
        self.texture     = arcade.load_texture(GameResources.get("textures") / "entity" / "player_highres.png")
        self.player_start    = BaseLevel.player_start(self, self.tile_map)
        self.collision_layers = level.collision_layers
        self.barrier_list     = self._build_barrier_list(level)


    def _build_barrier_list(self, level: BaseLevel) -> arcade.AStarBarrierList:
            # como va con sprites para las hitbox no se puede meter en la clase de nivel
            blocking_sprites = arcade.SpriteList()
            for name in level.collision_layers:
                blocking_sprites.extend(self.tile_map.sprite_lists[name])

            # no se puede hacer un A* para cada enemigo asi q hay q hacer todos loas enemigos de mas o menos el mismo tamaño
             # cambie el sprite de slime por un cuaadrado por q no furulaba con el zombie ese nuevo
            enemy = arcade.SpriteSolidColor(100, 100, arcade.color.WHITE)

            return arcade.AStarBarrierList(
                moving_sprite = enemy,
                blocking_sprites = blocking_sprites,
                grid_size = 64,
                left = int(level.bounds.left),
                right = int(level.bounds.right),
                bottom = int(level.bounds.bottom),
                top = int(level.bounds.top),
            )