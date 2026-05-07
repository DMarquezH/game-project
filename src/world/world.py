import arcade
from arcade import Scene, PhysicsEngineSimple, Sprite

from services.event_service import EventBus
from src.core.registry import TypeRegistry
from src.entities.player_entity import Player
from src.settings.game_constants import GameConstants
from src.settings.game_resources import GameResources
from src.world.systems.attack_system import AttackSystem


class World:

    def __init__(self, event_bus: EventBus):

        self.event_bus = event_bus

        self.systems = TypeRegistry()

        # A falta de implementar enemigos para parar su movimiento
        self.is_freeze = False

        self.scene: Scene | None = None
        self.player: Player | None = None
        self.physics: PhysicsEngineSimple | None = None

        self.init()

    def init(self):

        ### Systems ###

        self.systems.register(AttackSystem(self.event_bus))

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

        self.player = Player(self.event_bus, player_texture, 0.125)
        self.player.position = (GameConstants.WINDOW_WIDTH / 2, GameConstants.WINDOW_HEIGHT / 2)

        self.scene.add_sprite("player", self.player)

        ### Physics Engine ###

        self.physics = PhysicsEngineSimple(self.player, self.scene["trees"])

    def draw(self):
        self.scene.draw()

    def update(self):
        if not self.is_freeze:
            self.physics.update()

    def freeze(self):
        self.is_freeze = True

    def unfreeze(self):
        self.is_freeze = False

    def add_entity(self, entity: Sprite):
        pass