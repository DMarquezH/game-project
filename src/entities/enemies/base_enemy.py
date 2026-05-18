from abc import ABC, abstractmethod
import arcade
from pyglet.math import Vec2

from entities.base_entity import BaseEntity
from entities.player_entity import Player
from services.event_service import EventBus
from world.systems.movement.movement_events import EntityMoveEvent

class BaseEnemy(BaseEntity, ABC):
    PATH_RECALCULATE_INTERVAL = 0.5
    WAYPOINT_THRESHOLD        = 32

    def __init__( self, event_bus: EventBus, player: Player, barrier_list: arcade.AStarBarrierList):
        super().__init__(event_bus)
        self._player       = player
        self._barrier_list = barrier_list
        self._path: list[tuple[int, int]] = []
        self._path_timer   = 0.0
        self._setup_texture()
        self._setup_stats()

    # las estadisticas
    @abstractmethod
    def _setup_stats(self) -> None: ...

    @abstractmethod
    def update_behavior(self, delta_time: float) -> None: ...
    
    @abstractmethod
    def _setup_texture(self) -> None: ...

    # El movimiento es para todos x igual ya q el A* dice chatgpt q consume mucha memoria
    # y q no se puede hacer para cada enemigo
    def _recalculate_path(self) -> None:
        self._path = arcade.astar_calculate_path(
            start_point     = self.position,
            end_point       = self._player.position,
            astar_barrier_list = self._barrier_list,
            diagonal_movement = True
        ) or []

    def _follow_path(self) -> None:
        if not self._path:
            self._move_direct()
            return
        next_x, next_y = self._path[0]
        dx = next_x - self.center_x
        dy = next_y - self.center_y
        # si hay obstaculos hace los waypints esos y se va pa ellos
        if Vec2(dx, dy).length() < self.WAYPOINT_THRESHOLD:
            self._path.pop(0)
            return
        direction = Vec2(dx, dy).normalize()
        self.event_bus.dispatch(EntityMoveEvent(self, direction))

    def _get_distance_to_player(self) -> float:
        dx = self._player.center_x - self.center_x
        dy = self._player.center_y - self.center_y
        return Vec2(dx, dy).length()

    def _move_direct(self) -> None:
        dx = self._player.center_x - self.center_x
        dy = self._player.center_y - self.center_y
        direction = Vec2(dx, dy)
        if direction.length() > 0:
            self.event_bus.dispatch(EntityMoveEvent(self, direction.normalize()))

    def _stop(self) -> None:
        self.event_bus.dispatch(EntityMoveEvent(self, Vec2(0, 0)))
        
    def on_update(self, delta_time: float) -> None:
        self._path_timer += delta_time
        if self._path_timer >= self.PATH_RECALCULATE_INTERVAL:
            self._path_timer = 0.0
            self._recalculate_path()
        self._follow_path()
        self.update_behavior(delta_time)