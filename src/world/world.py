from typing import Dict, Type, Set
from pathlib import Path

import arcade
from arcade import Scene, PhysicsEngineSimple

from src.entities.base_entity import BaseEntity
from src.services.event_service import EventBus
from src.entities.player_entity import Player
from src.settings.game_resources import GameResources
from src.services.input.settings.registered_input_events import ToggleDebugInputEvent
from src.world.level.registered_levels import RegisteredLevels
from src.world.systems.combat.combat_system import CombatSystem
from src.world.systems.base_system import BaseSystem
from src.world.systems.movement.movement_system import MovementSystem, MovementMode
from src.world.level.base_level import BaseLevel
from src.world.level.level_loader import LevelLoader


class World:

    def __init__(self, event_bus: EventBus):

        self.current_level: BaseLevel | None = None
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
        self._subscribe_events()

        self.load_level(RegisteredLevels.CEMENTERY)

    def _init_systems(self):

        movement_system = MovementSystem(self.event_bus)
        combat_system = CombatSystem(self.event_bus)

        self.systems[MovementSystem] = movement_system
        self.systems[CombatSystem] = combat_system

        for system in self.systems.values():
            system.init()

    def load_level(self, level: BaseLevel) -> None:

        if self.current_level:
            self._unload()

        self.current_level = level
        data = LevelLoader(level)

        self._init_scene(data)
        self._init_player(data)
        self._init_physics(data)

    def _unload(self) -> None:

        self.scene = None
        self.player = None
        self.physics = None

        self.entities.clear()

    def _init_scene(self, data: LevelLoader):

        ### TILEMAP ###

        self.scene = Scene.from_tilemap(data.tile_map)

        ### SCENE ###

        self.scene.add_sprite_list_after("player", "Floor")

    def _init_player(self, data: LevelLoader):

        player_texture = arcade.load_texture(
            GameResources.get("textures") / "entity" / "player_highres.png"
        )

        self.player = Player(self.event_bus, player_texture, 0.125)
        self.player.position = data.player_start

        self.scene.add_sprite("player", self.player)

        movement_system: MovementSystem = self.systems.get(MovementSystem)
        movement_system.add_entity(self.player, MovementMode.FLOOR)

        self.entities.add(self.player)

    def _init_physics(self, data: LevelLoader):
        walls = [self.scene[name] for name in data.collision_layers]
        self.physics = PhysicsEngineSimple(self.player, walls, )

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

    def get_level_bounds(self) -> arcade.Rect:
        return self.current_level.bounds

    def toggle_debug(self, _: ToggleDebugInputEvent):
        self.debug = not self.debug

    def dispose(self):

        self._unsubscribe_events()

        for entity in self.entities:
            entity.dispose()

        for system in self.systems.values():
            system.dispose()