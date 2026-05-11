import arcade
from arcade import Scene, PhysicsEngineSimple

from src.services.event_service import EventBus
from src.core.registry import TypeRegistry
from src.entities.player_entity import Player
from src.settings.game_resources import GameResources
from src.services.input.settings.registered_input_events import ToggleDebugInputEvent
from src.world.systems.attack_system import AttackSystem
from src.world.systems.base_system import BaseSystem


class World:

    def __init__(self, event_bus: EventBus):

        self.event_bus = event_bus

        self.systems = TypeRegistry[BaseSystem]()

        self.scene: Scene | None = None
        self.player: Player | None = None
        self.physics: PhysicsEngineSimple | None = None

        self.debug = False

        self.init()

    def init(self):

        ### Systems ###

        self.systems.register(AttackSystem(self.event_bus))

        for system in self.systems.get_all().values():
            system.init()

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
        self.player.position = (0, 0)

        self.scene.add_sprite("player", self.player)

        ### Physics Engine ###

        self.physics = PhysicsEngineSimple(self.player, self.scene["trees"])

        ### Events ###

        self.event_bus.subscribe(ToggleDebugInputEvent, self.toggle_debug)

    def draw(self):

        self.scene.draw()

        if self.debug:
            self.scene.draw_hit_boxes(arcade.color.RED, 3)

    def update(self):
        self.player.update()
        self.physics.update()

    def toggle_debug(self, _: ToggleDebugInputEvent):
        self.debug = not self.debug