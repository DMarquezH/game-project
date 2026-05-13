from typing import Dict, Type, Set

import arcade
from arcade import Scene, PhysicsEngineSimple

from src.entities.base_entity import BaseEntity
from src.services.event_service import EventBus
from src.entities.player_entity import Player
from src.settings.game_resources import GameResources
from src.services.input.settings.registered_input_events import ToggleDebugInputEvent
from src.world.systems.combat.combat_system import CombatSystem
from src.world.systems.base_system import BaseSystem
from src.world.systems.movement.movement_system import MovementSystem, MovementMode


class World:

    def __init__(self, event_bus: EventBus):

        self.event_bus = event_bus

        self.scene: Scene | None = None
        self.player: Player | None = None
        self.physics: PhysicsEngineSimple | None = None

        self.entities: Set[BaseEntity] = set()
        self.systems: Dict[Type[BaseSystem], BaseSystem] = {}

        self.debug = False

        self.init()

    def init(self):

        self._init_systems()
        self._init_scene()
        self._init_player()
        self._subscribe_events()

        self.physics = PhysicsEngineSimple(self.player, [self.scene["Obstacles"], self.scene["Border"], self.scene["Border2"]])

    def _init_systems(self):

        movement_system = MovementSystem(self.event_bus)
        combat_system = CombatSystem(self.event_bus)

        self.systems[MovementSystem] = movement_system
        self.systems[CombatSystem] = combat_system

        for system in self.systems.values():
            system.init()

    def _init_scene(self):

        ### TILEMAP ###

        layer_options = {
            # Estan en orden de superposicion
            "Top2": {"use_spatial_hash": True},
            "top1": {"use_spatial_hash": True},
            "Border": {"use_spatial_hash": True},
            "Border2": {"use_spatial_hash": True},
            "Obstacles": {"use_spatial_hash": True}
        }

        tile_map = arcade.load_tilemap(
            GameResources.get("levels") / "level_2" / "LV2_1.0.tmj",
            scaling=1,
            layer_options=layer_options,
        )

        ### SCENE ###

        self.scene = Scene.from_tilemap(tile_map)
        self.scene.add_sprite_list_after("player", "Floor")

    def _init_player(self):

        player_texture = arcade.load_texture(
            GameResources.get("textures") / "entity" / "player_highres.png"
        )

        self.player = Player(self.event_bus, player_texture, 0.125)
        self.player.position = (500, 600)

        self.scene.add_sprite("player", self.player)

        movement_system: MovementSystem = self.systems.get(MovementSystem)
        movement_system.add_entity(self.player, MovementMode.FLOOR)

        self.entities.add(self.player)

    def _subscribe_events(self):
        self.event_bus.subscribe(ToggleDebugInputEvent, self.toggle_debug)

    def _unsubscribe_events(self):
        self.event_bus.unsubscribe(ToggleDebugInputEvent, self.toggle_debug)

    def update(self):

        self.physics.update()

        for system in self.systems.values():
            system.update()

    def draw(self):

        self.scene.draw()

        if self.debug:
            self.scene.draw_hit_boxes(arcade.color.RED, 3)

    def toggle_debug(self, _: ToggleDebugInputEvent):
        self.debug = not self.debug

    def dispose(self):

        self._unsubscribe_events()

        for entity in self.entities:
            entity.dispose()

        for system in self.systems.values():
            system.dispose()