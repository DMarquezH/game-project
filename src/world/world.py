import arcade
from arcade import Scene, Sprite, PhysicsEngineSimple, Camera2D
from pyglet.math import Vec2

from src.settings.game_constants import GameConstants
from src.settings.game_resources import GameResources


class World:

    def __init__(self):

        self.scene: Scene | None = None
        self.player: Sprite | None = None
        self.physics: PhysicsEngineSimple | None = None

        self.init()

    def init(self):

        ### Tilemap ###

        layer_options = {
            "trees": {  # Trees es el nombre de la capa de arboles en el tilemap
                "use_spatial_hash": True  # solo se revisarán las colisiones de los objetos cerca del jugador
            }
        }

        tile_map = arcade.load_tilemap(
            GameResources.get("levels") / "level_1" / "Test_map.tmj",
            scaling=1,
            layer_options=layer_options,
        )

        ### Scene ###

        self.scene = Scene.from_tilemap(tile_map)

        self.scene.add_sprite_list_after("player", "ground")

        ### Player ###

        player_texture = arcade.load_texture(
            GameResources.get("textures") / "entity" / "player_highres.png"
        )

        self.player = arcade.Sprite(player_texture, 0.125)
        self.player.position = (GameConstants.WINDOW_WIDTH / 2, GameConstants.WINDOW_HEIGHT / 2)

        self.scene.add_sprite("player", self.player)

        ### Physics Engine ###

        self.physics = PhysicsEngineSimple(self.player, self.scene["trees"])

    def draw(self):
        self.scene.draw()

    def update(self):
        self.physics.update()

    def move_player(self, move_dir: Vec2):
        self.player.change_x = 5 * move_dir.x
        self.player.change_y = 5 * move_dir.y

    def player_attack(self, attack_dir: Vec2):
        pass