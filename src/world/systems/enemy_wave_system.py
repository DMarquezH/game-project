import random
import arcade
from pyglet.math import Vec2

from entities.enemies.base_enemy import BaseEnemy
from entities.player_entity import Player
from services.event_service import EventBus
from world.systems.base_system import BaseSystem
from world.systems.movement.movement_system import MovementSystem, MovementMode
from world.systems.wave_definition import WaveDefinition, EnemySpawnEntry
from services.input.settings.registered_input_events import ViewportChangedEvent
from settings.registered_gameplay_events import EntityDeadEvent


class WaveCompleteEvent:
    pass

class AllWavesCompleteEvent:
    pass


class EnemyWaveSystem(BaseSystem):

    SPAWN_MARGIN = 80
    

    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus)

        self._waves: list[WaveDefinition] = []
        self._current_wave_index: int = -1
        self._spawn_queue: list[type[BaseEnemy]] = []
        self._active_enemies: set[BaseEnemy] = set()
        self._spawn_timer: float = 0.0
        self._current_interval: float = 1.0

        self._player: Player | None = None
        self._scene: arcade.Scene | None = None
        self._movement_system: MovementSystem | None = None
        self._barrier_list = None

    def init(self):
        # solo suscribe eventos, nada más
        if self._initialized: return
        super().init()

    def setup(
        self,
        waves: list[WaveDefinition],
        player: Player,
        scene: arcade.Scene,
        movement_system: MovementSystem,
        barrier_list=None,
    ):
        super().init()
        self._waves = waves
        self._player = player
        self._scene = scene
        self._movement_system = movement_system
        self._barrier_list = barrier_list
        self._viewport_w = 960.0   # valor por defecto hasta recibir el evento
        self._viewport_h = 540.0
        self.event_bus.subscribe(ViewportChangedEvent, self._on_viewport_changed)
        self.event_bus.subscribe(EntityDeadEvent, self._on_entity_dead)
        self._start_wave(0)

    def _on_viewport_changed(self, event: ViewportChangedEvent) -> None:
        self._viewport_w = event.width
        self._viewport_h = event.height

    def _start_wave(self, index: int) -> None:
        if index >= len(self._waves):
            self.event_bus.dispatch(AllWavesCompleteEvent())
            return

        self._current_wave_index = index
        wave = self._waves[index]
        self._current_interval = wave.spawn_interval
        self._spawn_timer = 0.0

        # construye la cola de spawns
        self._spawn_queue.clear()
        for entry in wave.entries:
            self._spawn_queue.extend([entry.enemy_type] * entry.count)
        random.shuffle(self._spawn_queue)

    def _advance_wave(self):
        self.event_bus.dispatch(WaveCompleteEvent())
        self._start_wave(self._current_wave_index + 1)

    def update(self):
        pass

    def on_update(self, delta_time: float):
        self._try_spawn(delta_time)
        self._check_wave_complete()

    def _try_spawn(self, delta_time: float):
        if not self._spawn_queue:
            return

        self._spawn_timer += delta_time
        if self._spawn_timer >= self._current_interval:
            self._spawn_timer = 0.0
            enemy_type = self._spawn_queue.pop(0)
            self._spawn_enemy(enemy_type)

    def _check_wave_complete(self):
        if self._spawn_queue:
            return
        if not self._active_enemies:
            self._advance_wave()

    # --- Spawn ---

    def _spawn_enemy(self, enemy_type: type[BaseEnemy]):
        position = self._get_spawn_position()

        enemy = enemy_type(event_bus = self.event_bus, player = self._player, barrier_list = self._barrier_list,)
        enemy.position = position

        self._scene.add_sprite("Enemies", enemy)
        self._movement_system.add_entity(enemy, MovementMode.FLOOR)
        self._active_enemies.add(enemy)

    def _get_spawn_position(self) -> tuple[float, float]:
        cx, cy = self._player.position
        half_w = self._viewport_w / 2 + self.SPAWN_MARGIN
        half_h = self._viewport_h / 2 + self.SPAWN_MARGIN

        side = random.randint(0, 3)
        if side == 0:
            return (random.uniform(cx - half_w, cx + half_w), cy + half_h)
        elif side == 1:
            return (random.uniform(cx - half_w, cx + half_w), cy - half_h)
        elif side == 2:
            return (cx - half_w, random.uniform(cy - half_h, cy + half_h))
        else:
            return (cx + half_w, random.uniform(cy - half_h, cy + half_h))

    def _on_entity_dead(self, event) -> None:
        entity = event.entity
        if isinstance(entity, BaseEnemy):
            self._active_enemies.discard(entity)
            self._movement_system.remove_entity(entity)
            entity.kill()
            self._check_wave_complete()
        elif isinstance(entity, Player):
            print("GAME OVER")
            # GameOverEvent() o asi pero me dio pereza
            entity.kill()

    def dispose(self) -> None:
        self.event_bus.unsubscribe(ViewportChangedEvent, self._on_viewport_changed)
        from settings.registered_gameplay_events import EntityDeadEvent
        self.event_bus.unsubscribe(EntityDeadEvent, self._on_entity_dead)
